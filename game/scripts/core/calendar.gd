class_name Calendar
extends RefCounted

# US-English wording for ISO dates ("2003-10-15").
const WEEKDAYS := ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
const MONTHS := ["January","February","March","April","May","June","July","August","September","October","November","December"]

static func weekday(date: String) -> String:
	var unix := Time.get_unix_time_from_datetime_string(date)
	return WEEKDAYS[int(Time.get_datetime_dict_from_unix_time(unix).weekday)]

static func day_number(date: String) -> int:
	return int(date.split("-")[2])

# "October 15"
static func month_day(date: String) -> String:
	var parts := date.split("-")
	return "%s %d" % [MONTHS[int(parts[1])-1],int(parts[2])]

# "Wednesday, October 15"
static func long_date(date: String) -> String:
	return weekday(date)+", "+month_day(date)

# "October 15, 2003"
static func full_date(date: String) -> String:
	return month_day(date)+", "+date.left(4)
