from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import pytz
from typing import Optional, List
from dateutil import parser
import json
import urllib.parse

app = FastAPI(
    title="Time Zone Converter API",
    description="An API for converting times between different time zones with advanced features",
    version="2.0.0"
)

class TimeZoneConversion(BaseModel):
    datetime: str
    source_timezone: str
    target_timezone: str

class TimeZoneResponse(BaseModel):
    source_time: str
    source_timezone: str
    converted_time: str
    target_timezone: str

class BatchConversion(BaseModel):
    conversions: List[TimeZoneConversion]

class BatchResponse(BaseModel):
    results: List[TimeZoneResponse]

class TimeZoneInfo(BaseModel):
    timezone: str
    current_time: str
    utc_offset: str
    is_dst: bool
    dst_name: str

def decode_timezone(timezone: str) -> str:
    """Decode URL-encoded timezone name."""
    try:
        return urllib.parse.unquote(timezone)
    except:
        return timezone

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Enhanced Time Zone Converter API",
        "version": "2.0.0",
        "endpoints": {
            "/timezones": "Get list of all available timezones",
            "/timezones/search": "Search timezones by name",
            "/convert": "Convert time between different timezones",
            "/convert/batch": "Convert multiple times at once",
            "/current/{timezone}": "Get current time in a specific timezone",
            "/current": "Get current time in multiple timezones",
            "/info/{timezone}": "Get detailed timezone information"
        }
    }

@app.get("/timezones")
async def get_timezones():
    """Get a list of all available timezones."""
    return {"timezones": pytz.all_timezones}

@app.get("/timezones/search")
async def search_timezones(q: str = Query(..., min_length=1, description="Search term for timezone")):
    """Search timezones by name."""
    search_term = q.lower()
    matching_timezones = [
        tz for tz in pytz.all_timezones 
        if search_term in tz.lower()
    ]
    return {
        "search_term": q,
        "results": matching_timezones,
        "count": len(matching_timezones)
    }

@app.get("/current/{timezone:path}")
async def get_current_time(timezone: str):
    """Get current time in a specific timezone."""
    try:
        # Decode the timezone parameter
        decoded_timezone = decode_timezone(timezone)
        
        if decoded_timezone not in pytz.all_timezones:
            raise HTTPException(status_code=400, detail=f"Invalid timezone: {decoded_timezone}")
        
        tz = pytz.timezone(decoded_timezone)
        current_time = datetime.now(tz)
        
        return {
            "timezone": decoded_timezone,
            "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "utc_offset": current_time.strftime("%z"),
            "is_dst": current_time.dst() != None and current_time.dst().total_seconds() > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/current")
async def get_current_time_multiple(
    timezones: str = Query(..., description="Comma-separated list of timezones")
):
    """Get current time in multiple timezones."""
    try:
        tz_list = [tz.strip() for tz in timezones.split(",")]
        results = []
        
        for tz_name in tz_list:
            if tz_name not in pytz.all_timezones:
                results.append({
                    "timezone": tz_name,
                    "error": "Invalid timezone"
                })
                continue
            
            tz = pytz.timezone(tz_name)
            current_time = datetime.now(tz)
            
            results.append({
                "timezone": tz_name,
                "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "utc_offset": current_time.strftime("%z"),
                "is_dst": current_time.dst() != None and current_time.dst().total_seconds() > 0
            })
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/info/{timezone:path}")
async def get_timezone_info(timezone: str):
    """Get detailed information about a specific timezone."""
    try:
        # Decode the timezone parameter
        decoded_timezone = decode_timezone(timezone)
        
        if decoded_timezone not in pytz.all_timezones:
            raise HTTPException(status_code=400, detail=f"Invalid timezone: {decoded_timezone}")
        
        tz = pytz.timezone(decoded_timezone)
        # Use a naive datetime for utcoffset and dst
        now_utc = datetime.utcnow()
        localized_dt = tz.localize(now_utc)
        tz_info = localized_dt.utcoffset()
        dst_info = localized_dt.dst()
        
        return TimeZoneInfo(
            timezone=decoded_timezone,
            current_time=localized_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
            utc_offset=f"{int(tz_info.total_seconds()/3600):+03d}:{int((tz_info.total_seconds()%3600)/60):02d}",
            is_dst=dst_info.total_seconds() > 0 if dst_info else False,
            dst_name=localized_dt.tzname()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert", response_model=TimeZoneResponse)
async def convert_timezone(conversion: TimeZoneConversion):
    """
    Convert time from one timezone to another.
    
    Parameters:
    - datetime: Time to convert (format: "YYYY-MM-DD HH:MM:SS")
    - source_timezone: Source timezone
    - target_timezone: Target timezone
    """
    try:
        # Validate timezones
        if conversion.source_timezone not in pytz.all_timezones:
            raise HTTPException(status_code=400, detail=f"Invalid source timezone: {conversion.source_timezone}")
        if conversion.target_timezone not in pytz.all_timezones:
            raise HTTPException(status_code=400, detail=f"Invalid target timezone: {conversion.target_timezone}")

        # Parse the input datetime
        try:
            dt = parser.parse(conversion.datetime)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS")

        # Create timezone objects
        source_tz = pytz.timezone(conversion.source_timezone)
        target_tz = pytz.timezone(conversion.target_timezone)

        # Localize the datetime to source timezone
        source_dt = source_tz.localize(dt)
        
        # Convert to target timezone
        target_dt = source_dt.astimezone(target_tz)

        return TimeZoneResponse(
            source_time=source_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
            source_timezone=conversion.source_timezone,
            converted_time=target_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
            target_timezone=conversion.target_timezone
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert/batch", response_model=BatchResponse)
async def convert_timezone_batch(batch: BatchConversion):
    """
    Convert multiple times between different timezones in a single request.
    """
    try:
        results = []
        
        for conversion in batch.conversions:
            try:
                # Validate timezones
                if conversion.source_timezone not in pytz.all_timezones:
                    results.append(TimeZoneResponse(
                        source_time="ERROR",
                        source_timezone=conversion.source_timezone,
                        converted_time=f"Invalid source timezone: {conversion.source_timezone}",
                        target_timezone=conversion.target_timezone
                    ))
                    continue
                    
                if conversion.target_timezone not in pytz.all_timezones:
                    results.append(TimeZoneResponse(
                        source_time="ERROR",
                        source_timezone=conversion.source_timezone,
                        converted_time=f"Invalid target timezone: {conversion.target_timezone}",
                        target_timezone=conversion.target_timezone
                    ))
                    continue

                # Parse the input datetime
                try:
                    dt = parser.parse(conversion.datetime)
                except ValueError:
                    results.append(TimeZoneResponse(
                        source_time="ERROR",
                        source_timezone=conversion.source_timezone,
                        converted_time="Invalid datetime format",
                        target_timezone=conversion.target_timezone
                    ))
                    continue

                # Create timezone objects
                source_tz = pytz.timezone(conversion.source_timezone)
                target_tz = pytz.timezone(conversion.target_timezone)

                # Localize the datetime to source timezone
                source_dt = source_tz.localize(dt)
                
                # Convert to target timezone
                target_dt = source_dt.astimezone(target_tz)

                results.append(TimeZoneResponse(
                    source_time=source_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
                    source_timezone=conversion.source_timezone,
                    converted_time=target_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
                    target_timezone=conversion.target_timezone
                ))
                
            except Exception as e:
                results.append(TimeZoneResponse(
                    source_time="ERROR",
                    source_timezone=conversion.source_timezone,
                    converted_time=str(e),
                    target_timezone=conversion.target_timezone
                ))
        
        return BatchResponse(results=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 