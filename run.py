import json
import logging
import datetime as dt
from urllib import request
from swhen.mapping import Mapping
from swhen.assesor import Assesor
from config import Configuration
from jsonschema.exceptions import ValidationError
from jsonschema import validate

URL = "http://magicseaweed.com/api/{0}/forecast/?spot_id={1}"


def convert_timestamp_to_real_date(timestamp):
    return dt.datetime.fromtimestamp(timestamp).ctime()


def get_data_from_obj(_obj: dict):
    response_schema = {
        "type": "object",
        "properties": {
            "swell": {"type": "object"},
            "wind": {"type": "object"},
            "condition": {"type": "object"},
            "solidRating": {"type": "number"},
            "fadedRating": {"type": "number"}
        }
    }
    try:
        validate(instance=_obj, schema=response_schema)
    except ValidationError as e:
        logger.error(f"Response json isn't valid, {e}")
        return False
    return {
        'min_break': _obj['swell']['absMinBreakingHeight'],
        'max_break': _obj['swell']['absMaxBreakingHeight'],
        'probability':_obj['swell']['probability'],
        'period': _obj['swell']['components']['combined']['period'],
        'wind': _obj['wind']['speed'],
        'water_temp': _obj['condition']['temperature'],
        'solidRating': _obj['solidRating'],
        'fadedRating': _obj['fadedRating'],
        'date': convert_timestamp_to_real_date(_obj['timestamp'])
    }


def filter_and_parse_resp(response, spot):
    logger.info(f"started to filter and parse response")
    non_optional_hours = ["00:00:00", "21:00:00", "03:00:00"]
    ret_json = {
        spot: {}
    }
    for _obj in response:
        timestamp_str = str(_obj['timestamp'])
        date_time_str = convert_timestamp_to_real_date(_obj['timestamp'])
        logger.info(f"Going over: {date_time_str}")
        skip_obj = False
        for hour in non_optional_hours:
            if hour in date_time_str:
                skip_obj = True
                logger.info(f"session is off surfing hours, skip to next session")
                break

        if skip_obj: continue
        logger.info(f"start to assess session {date_time_str}")
        assess = Assesor(_obj).assess_session()
        logger.info(f" session {date_time_str} as been assessed, score: {assess}")
        if assess > 20:
            ret_json[spot][timestamp_str] = get_data_from_obj(_obj)
            logger.info(f" session {date_time_str} added to recommendation json")

    return ret_json


def main():
    logger.info("Loading configuration")
    conf = Configuration("config/API_conf.json")

    for i in range(len(conf.spots)):
        current_spot = conf.spots[i]
        city = Mapping().get_city(current_spot)
        logger.info(f"surf check started for {city}")
        try:
            logger.info(f"request for swell broadcast")
            with request.urlopen(URL.format(conf.token, current_spot)) as resp:
                data = resp.read()
                logger.info(f"request succeeded")
            k = filter_and_parse_resp(json.loads(data.decode('utf-8')), city)

            with open(f"Swell_{city.lower()}.json", "a") as f:
                f.write(json.dumps(k))

        except Exception as e:
            print("NOT GOOD: ", e)


if __name__ == '__main__':
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=rf"/Users/eliorc/PycharmProjects/Swhen/logs/log_{dt.datetime.now()}.log",
                        level=logging.DEBUG,
                        format=LOG_FORMAT)
    logger = logging.getLogger()
    main()
    # TODO: no need to iterate over off hours sessions, so just match hours with datetime and iterate only 6-18