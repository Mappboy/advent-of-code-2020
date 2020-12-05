"""
Now we should be able to use regex to parse the file but whatever.
This would be prefect for something like pydantic
"""
import re
from pathlib import Path

test = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

invalid_tests = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

valid_tests = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

field_tests = """
byr valid:   2002
byr invalid: 2003

hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190

hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc

ecl valid:   brn
ecl invalid: wat

pid valid:   000000001
pid invalid: 0123456789
"""
test_re = re.compile(r"(?P<key>\w{3})\s+(?P<test>invalid|valid):\s+(?P<value>#?\w+)")
EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
RECORDS = re.compile(r"(?P<key>\w{3}):(?P<value>#?\w+)[\b\n]?")

CID = "cid"


def valid_height(height):
    if re.match(r"(\d+)(cm|in)", height):
        cms = re.match(r"(\d+)(cm)", height)
        inches = re.match(r"(\d+)(in)", height)
        if cms:
            return 150 <= int(cms.groups()[0]) <= 193
        else:
            return 59 <= int(inches.groups()[0]) <= 76
    return False


REQ_FIELDS = {"byr": lambda x: 1920 <= int(x) <= 2002,
              "iyr": lambda x: 2010 <= int(x) <= 2020,
              "eyr": lambda x: re.match(r"\d{4}", x) and 2020 <= int(x) <= 2030,
              "hgt": valid_height,
              "hcl": lambda x: bool(re.match(r"#[0-9a-f]{6}", x)),
              "ecl": lambda x: x in EYE_COLORS,
              "pid": lambda x: re.match(r"\d{9}", x) and len(x) == 9,
              }
REQ_FIELDS_SET = set(REQ_FIELDS.keys())


def check_valid(passport_details: dict):
    details = [(key, REQ_FIELDS[key](value)) for key, value in passport_details.items() if key != CID]

    return all([_[1] for _ in details])


def parse_batch(input_str):
    valids = 0
    for batch in input_str.split("\n\n"):
        passport = {}
        for pairs in RECORDS.findall(batch):
            passport[pairs[0]] = pairs[1]
        if not REQ_FIELDS_SET.difference(passport.keys()):
            valids += 1
    return valids


def parse_and_validate_batch(input_str):
    valids = 0
    for batch in input_str.split("\n\n"):
        passport = {}
        for pairs in RECORDS.findall(batch):
            passport[pairs[0]] = pairs[1]
        if not REQ_FIELDS_SET.difference(passport.keys()) and check_valid(passport):
            valids += 1
    return valids


if __name__ == '__main__':
    bt = parse_batch(test)
    assert bt == 2
    assert parse_and_validate_batch(invalid_tests) == 0
    assert parse_and_validate_batch(valid_tests) == 4
    ind_tests = [REQ_FIELDS[_[0]](_[2]) == (_[1] == "valid") for _ in test_re.findall(field_tests)]
    assert all(ind_tests)
    with open(Path("inputs").joinpath("day4.txt"), "r") as input_data:
        lines = input_data.read()
        print(parse_batch(lines))
        print(parse_and_validate_batch(lines))
