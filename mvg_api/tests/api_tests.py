import datetime
from typing import List

from mvg_api.api.api import Api
from mvg_api.mvg import LocationNotFound
from mvg_api.models.route import LocationList, LocationType, Connections
from mvg_api.models.ticker import TickerList, SlimList


def test_get_ticker():
    api = Api()
    response = api.get_ticker()
    assert isinstance(response, TickerList)


def test_get_current_date():
    api = Api()
    response = api.get_current_date()
    assert isinstance(response, datetime.datetime)


def test_get_station_global_ids():
    api = Api()
    station_ids = [
        "de:09162:1",
        "de:09162:2",
        "de:09162:3",
        "de:09162:4",
        "de:09162:5",
        "de:09162:6",
        "de:09162:7",
        "de:09162:8",
        "de:09162:9",
        "de:09162:10",
        "de:09162:11",
        "de:09162:12",
        "de:09162:13",
        "de:09162:15",
        "de:09162:16",
        "de:09162:17",
        "de:09162:18",
        "de:09162:19",
        "de:09162:20",
        "de:09162:21",
        "de:09162:22",
        "de:09162:23",
        "de:09162:25",
        "de:09162:26",
        "de:09162:27",
        "de:09162:29",
        "de:09162:30",
        "de:09162:31",
        "de:09162:32",
        "de:09162:34",
        "de:09162:35",
        "de:09162:36",
        "de:09162:38",
        "de:09162:40",
        "de:09162:41",
        "de:09162:42",
        "de:09162:43",
        "de:09162:44",
        "de:09162:45",
        "de:09162:46",
        "de:09162:47",
        "de:09162:48",
        "de:09162:49",
        "de:09162:50",
        "de:09162:51",
        "de:09162:52",
        "de:09162:53",
        "de:09162:54",
        "de:09162:55",
        "de:09162:56",
        "de:09162:57",
        "de:09162:58",
        "de:09162:59",
        "de:09162:60",
        "de:09162:61",
        "de:09162:62",
        "de:09162:63",
        "de:09162:64",
        "de:09162:65",
        "de:09162:66",
        "de:09162:67",
        "de:09162:68",
        "de:09162:70",
        "de:09162:73",
        "de:09162:74",
        "de:09162:75",
        "de:09162:76",
        "de:09162:77",
        "de:09162:78",
        "de:09162:79",
        "de:09162:80",
        "de:09162:81",
        "de:09162:82",
        "de:09162:83",
        "de:09162:84",
        "de:09162:85",
        "de:09162:86",
        "de:09162:87",
        "de:09162:88",
        "de:09162:89",
        "de:09162:90",
        "de:09162:91",
        "de:09162:92",
        "de:09162:93",
        "de:09162:95",
        "de:09162:96",
        "de:09162:97",
        "de:09162:101",
        "de:09162:102",
        "de:09162:103",
        "de:09162:104",
        "de:09162:105",
        "de:09162:106",
        "de:09162:107",
        "de:09162:108",
        "de:09162:109",
        "de:09162:110",
        "de:09162:111",
        "de:09162:112",
        "de:09162:113",
        "de:09162:114",
        "de:09162:115",
        "de:09162:116",
        "de:09162:117",
        "de:09162:118",
        "de:09162:119",
        "de:09162:120",
        "de:09162:121",
        "de:09162:122",
        "de:09162:123",
        "de:09162:124",
        "de:09162:125",
        "de:09162:126",
        "de:09162:127",
        "de:09162:128",
        "de:09162:129",
        "de:09162:130",
        "de:09162:131",
        "de:09162:132",
        "de:09162:133",
        "de:09162:134",
        "de:09162:135",
        "de:09162:136",
        "de:09162:137",
        "de:09162:138",
        "de:09162:139",
        "de:09162:140",
        "de:09162:141",
        "de:09162:142",
        "de:09162:143",
        "de:09162:144",
        "de:09162:146",
        "de:09162:150",
        "de:09162:151",
        "de:09162:152",
        "de:09162:153",
        "de:09162:156",
        "de:09162:157",
        "de:09162:158",
        "de:09162:159",
        "de:09162:160",
        "de:09162:161",
        "de:09162:162",
        "de:09162:163",
        "de:09162:164",
        "de:09162:165",
        "de:09162:166",
        "de:09162:170",
        "de:09162:180",
        "de:09162:185",
        "de:09162:190",
        "de:09162:197",
        "de:09162:200",
        "de:09162:204",
        "de:09162:205",
        "de:09162:206",
        "de:09162:207",
        "de:09162:209",
        "de:09162:210",
        "de:09162:211",
        "de:09162:212",
        "de:09162:213",
        "de:09162:214",
        "de:09162:215",
        "de:09162:216",
        "de:09162:217",
        "de:09162:218",
        "de:09162:219",
        "de:09162:220",
        "de:09162:221",
        "de:09162:222",
        "de:09162:223",
        "de:09162:224",
        "de:09162:225",
        "de:09162:226",
        "de:09162:227",
        "de:09162:228",
        "de:09162:229",
        "de:09162:230",
        "de:09162:231",
        "de:09162:232",
        "de:09162:233",
        "de:09162:234",
        "de:09162:235",
        "de:09162:236",
        "de:09162:237",
        "de:09162:238",
        "de:09162:239",
        "de:09162:240",
        "de:09162:250",
        "de:09162:251",
        "de:09162:260",
        "de:09162:270",
        "de:09162:280",
        "de:09162:285",
        "de:09162:290",
        "de:09162:291",
        "de:09162:292",
        "de:09162:293",
        "de:09162:294",
        "de:09162:296",
        "de:09162:299",
        "de:09162:300",
        "de:09162:301",
        "de:09162:302",
        "de:09162:303",
        "de:09162:304",
        "de:09162:305",
        "de:09162:306",
        "de:09162:307",
        "de:09162:308",
        "de:09162:309",
        "de:09162:310",
        "de:09162:311",
        "de:09162:312",
        "de:09162:313",
        "de:09162:314",
        "de:09162:316",
        "de:09162:318",
        "de:09162:319",
        "de:09162:320",
        "de:09162:321",
        "de:09162:322",
        "de:09162:323",
        "de:09162:324",
        "de:09162:325",
        "de:09162:326",
        "de:09162:328",
        "de:09162:329",
        "de:09162:330",
        "de:09162:331",
        "de:09162:333",
        "de:09162:334",
        "de:09162:335",
        "de:09162:336",
        "de:09162:337",
        "de:09162:338",
        "de:09162:340",
        "de:09162:341",
        "de:09162:342",
        "de:09162:343",
        "de:09162:344",
        "de:09162:346",
        "de:09162:349",
        "de:09162:350",
        "de:09162:351",
        "de:09162:352",
        "de:09162:353",
        "de:09162:354",
        "de:09162:355",
        "de:09162:356",
        "de:09162:357",
        "de:09162:358",
        "de:09162:359",
        "de:09162:360",
        "de:09162:363",
        "de:09162:366",
        "de:09162:368",
        "de:09162:369",
        "de:09162:370",
        "de:09162:376",
        "de:09162:377",
        "de:09162:380",
        "de:09162:381",
        "de:09162:382",
        "de:09162:383",
        "de:09162:384",
        "de:09162:385",
        "de:09162:396",
        "de:09162:397",
        "de:09162:398",
        "de:09162:399",
        "de:09162:400",
        "de:09162:401",
        "de:09162:402",
        "de:09162:404",
        "de:09162:405",
        "de:09162:406",
        "de:09162:407",
        "de:09162:408",
        "de:09162:409",
        "de:09162:410",
        "de:09162:413",
        "de:09162:414",
        "de:09162:415",
        "de:09162:416",
        "de:09162:417",
        "de:09162:418",
        "de:09162:419",
        "de:09162:420",
        "de:09162:421",
        "de:09162:422",
        "de:09162:423",
        "de:09162:424",
        "de:09162:425",
        "de:09162:426",
        "de:09162:427",
        "de:09162:428",
        "de:09162:429",
        "de:09162:430",
        "de:09162:431",
        "de:09162:432",
        "de:09162:433",
        "de:09162:434",
        "de:09162:435",
        "de:09162:436",
        "de:09162:437",
        "de:09162:438",
        "de:09162:439",
        "de:09162:440",
        "de:09162:441",
        "de:09162:442",
        "de:09162:443",
        "de:09162:444",
        "de:09162:445",
        "de:09162:446",
        "de:09162:447",
        "de:09162:448",
        "de:09162:449",
        "de:09162:451",
        "de:09162:452",
        "de:09162:453",
        "de:09162:454",
        "de:09162:455",
        "de:09162:457",
        "de:09162:458",
        "de:09162:459",
        "de:09184:460",
        "de:09162:463",
        "de:09162:464",
        "de:09162:465",
        "de:09162:466",
        "de:09162:470",
        "de:09184:480",
        "de:09184:490",
        "de:09162:500",
        "de:09162:501",
        "de:09162:502",
        "de:09162:503",
        "de:09162:510",
        "de:09162:511",
        "de:09162:512",
        "de:09162:513",
        "de:09162:518",
        "de:09162:520",
        "de:09162:530",
        "de:09162:540",
        "de:09162:541",
        "de:09162:542",
        "de:09162:543",
        "de:09162:544",
        "de:09162:545",
        "de:09162:546",
        "de:09162:548",
        "de:09162:549",
        "de:09162:550",
        "de:09162:551",
        "de:09162:552",
        "de:09162:553",
        "de:09162:554",
        "de:09162:555",
        "de:09162:556",
        "de:09162:557",
        "de:09162:560",
        "de:09162:570",
        "de:09162:580",
        "de:09162:581",
        "de:09162:590",
        "de:09162:599",
        "de:09162:600",
        "de:09162:601",
        "de:09162:602",
        "de:09162:603",
        "de:09162:604",
        "de:09162:605",
        "de:09162:606",
        "de:09162:607",
        "de:09162:608",
        "de:09162:609",
        "de:09162:610",
        "de:09162:611",
        "de:09162:612",
        "de:09162:613",
        "de:09162:615",
        "de:09162:616",
        "de:09162:617",
        "de:09162:618",
        "de:09162:619",
        "de:09162:620",
        "de:09162:621",
        "de:09162:622",
        "de:09162:623",
        "de:09162:624",
        "de:09162:625",
        "de:09162:626",
        "de:09162:627",
        "de:09162:628",
        "de:09162:629",
        "de:09162:632",
        "de:09162:633",
        "de:09162:634",
        "de:09162:635",
        "de:09162:636",
        "de:09162:637",
        "de:09162:638",
        "de:09162:640",
        "de:09162:641",
        "de:09162:642",
        "de:09162:643",
        "de:09162:646",
        "de:09162:648",
        "de:09162:650",
        "de:09162:651",
        "de:09162:652",
        "de:09162:653",
        "de:09162:654",
        "de:09162:655",
        "de:09162:656",
        "de:09162:657",
        "de:09162:662",
        "de:09162:663",
        "de:09162:670",
        "de:09162:671",
        "de:09162:680",
        "de:09162:698",
        "de:09162:699",
        "de:09162:701",
        "de:09162:702",
        "de:09162:703",
        "de:09162:704",
        "de:09162:705",
        "de:09162:720",
        "de:09162:721",
        "de:09162:725",
        "de:09162:727",
        "de:09162:728",
        "de:09162:730",
        "de:09162:731",
        "de:09162:740",
        "de:09162:745",
        "de:09162:750",
        "de:09162:751",
        "de:09162:752",
        "de:09162:753",
        "de:09162:754",
        "de:09162:755",
        "de:09162:756",
        "de:09162:757",
        "de:09162:758",
        "de:09162:760",
        "de:09162:762",
        "de:09162:767",
        "de:09162:768",
        "de:09162:769",
        "de:09162:770",
        "de:09162:771",
        "de:09162:780",
        "de:09162:788",
        "de:09162:790",
        "de:09162:792",
        "de:09162:800",
        "de:09162:801",
        "de:09162:802",
        "de:09162:803",
        "de:09162:805",
        "de:09162:807",
        "de:09162:808",
        "de:09162:809",
        "de:09162:810",
        "de:09162:811",
        "de:09162:813",
        "de:09162:814",
        "de:09162:815",
        "de:09162:816",
        "de:09162:817",
        "de:09162:818",
        "de:09162:819",
        "de:09162:824",
        "de:09162:825",
        "de:09162:890",
        "de:09162:891",
        "de:09162:892",
        "de:09162:893",
        "de:09162:894",
        "de:09162:895",
        "de:09162:896",
        "de:09162:897",
        "de:09162:898",
        "de:09162:899",
        "de:09162:901",
        "de:09162:902",
        "de:09162:903",
        "de:09162:904",
        "de:09162:906",
        "de:09162:907",
        "de:09162:908",
        "de:09162:909",
        "de:09162:910",
        "de:09162:911",
        "de:09162:912",
        "de:09162:913",
        "de:09162:914",
        "de:09162:915",
        "de:09162:916",
        "de:09162:917",
        "de:09162:920",
        "de:09162:921",
        "de:09162:923",
        "de:09162:926",
        "de:09162:927",
        "de:09162:928",
        "de:09162:929",
        "de:09162:930",
        "de:09162:931",
        "de:09162:932",
        "de:09162:933",
        "de:09162:934",
        "de:09162:935",
        "de:09162:936",
        "de:09162:937",
        "de:09162:938",
        "de:09162:939",
        "de:09162:940",
        "de:09162:941",
        "de:09162:942",
        "de:09162:943",
        "de:09162:944",
        "de:09162:945",
        "de:09162:946",
        "de:09162:947",
        "de:09162:948",
        "de:09162:949",
        "de:09162:950",
        "de:09162:951",
        "de:09162:952",
        "de:09162:953",
        "de:09162:954",
        "de:09162:955",
        "de:09162:956",
        "de:09162:957",
        "de:09162:958",
        "de:09162:959",
        "de:09162:960",
        "de:09162:961",
        "de:09162:962",
        "de:09162:963",
        "de:09162:964",
        "de:09162:965",
        "de:09162:966",
        "de:09162:967",
        "de:09162:969",
        "de:09162:970",
        "de:09162:971",
        "de:09162:972",
        "de:09162:973",
        "de:09162:974",
        "de:09162:975",
        "de:09162:976",
        "de:09162:977",
        "de:09162:978",
        "de:09162:979",
        "de:09162:981",
        "de:09162:983",
        "de:09162:988",
        "de:09162:989",
        "de:09162:990",
        "de:09162:991",
        "de:09162:993",
        "de:09162:994",
        "de:09162:995",
        "de:09162:997",
        "de:09162:998",
        "de:09162:999",
        "de:09162:1000",
        "de:09162:1001",
        "de:09162:1002",
        "de:09162:1003",
        "de:09162:1004",
        "de:09162:1005",
        "de:09162:1006",
        "de:09162:1007",
        "de:09162:1008",
        "de:09162:1009",
        "de:09162:1010",
        "de:09162:1011",
        "de:09162:1012",
        "de:09162:1013",
        "de:09162:1014",
        "de:09162:1015",
        "de:09162:1016",
        "de:09162:1017",
        "de:09162:1018",
        "de:09162:1019",
        "de:09162:1020",
        "de:09162:1021",
        "de:09162:1022",
        "de:09162:1023",
        "de:09162:1024",
        "de:09162:1025",
        "de:09162:1026",
        "de:09162:1027",
        "de:09162:1028",
        "de:09162:1029",
        "de:09162:1030",
        "de:09162:1031",
        "de:09162:1032",
        "de:09162:1033",
        "de:09162:1034",
        "de:09162:1035",
        "de:09162:1036",
        "de:09162:1037",
        "de:09162:1038",
        "de:09162:1039",
        "de:09162:1040",
        "de:09162:1041",
        "de:09162:1042",
        "de:09162:1043",
        "de:09162:1044",
        "de:09162:1045",
        "de:09162:1046",
        "de:09162:1047",
        "de:09162:1048",
        "de:09162:1050",
        "de:09162:1053",
        "de:09162:1054",
        "de:09162:1055",
        "de:09162:1056",
        "de:09162:1057",
        "de:09162:1058",
        "de:09162:1059",
        "de:09162:1060",
        "de:09162:1061",
        "de:09162:1062",
        "de:09162:1064",
        "de:09162:1070",
        "de:09162:1101",
        "de:09162:1102",
        "de:09162:1103",
        "de:09162:1104",
        "de:09162:1105",
        "de:09162:1106",
        "de:09162:1107",
        "de:09162:1108",
        "de:09162:1109",
        "de:09162:1110",
        "de:09162:1111",
        "de:09162:1112",
        "de:09162:1115",
        "de:09162:1117",
        "de:09162:1118",
        "de:09162:1119",
        "de:09162:1120",
        "de:09162:1121",
        "de:09162:1122",
        "de:09162:1123",
        "de:09162:1124",
        "de:09162:1125",
        "de:09162:1126",
        "de:09162:1128",
        "de:09162:1129",
        "de:09162:1130",
        "de:09162:1131",
        "de:09162:1132",
        "de:09162:1133",
        "de:09162:1134",
        "de:09162:1135",
        "de:09162:1139",
        "de:09162:1140",
        "de:09162:1141",
        "de:09162:1142",
        "de:09162:1143",
        "de:09162:1144",
        "de:09162:1145",
        "de:09162:1146",
        "de:09162:1148",
        "de:09162:1149",
        "de:09162:1150",
        "de:09162:1151",
        "de:09162:1152",
        "de:09162:1154",
        "de:09162:1156",
        "de:09162:1157",
        "de:09162:1158",
        "de:09162:1159",
        "de:09162:1160",
        "de:09162:1161",
        "de:09162:1162",
        "de:09162:1163",
        "de:09162:1165",
        "de:09162:1166",
        "de:09162:1167",
        "de:09162:1168",
        "de:09162:1169",
        "de:09162:1170",
        "de:09162:1171",
        "de:09162:1172",
        "de:09162:1173",
        "de:09162:1174",
        "de:09162:1177",
        "de:09162:1178",
        "de:09162:1179",
        "de:09162:1180",
        "de:09162:1181",
        "de:09162:1182",
        "de:09162:1183",
        "de:09162:1184",
        "de:09162:1185",
        "de:09162:1187",
        "de:09162:1189",
        "de:09162:1190",
        "de:09162:1191",
        "de:09162:1192",
        "de:09162:1200",
        "de:09162:1201",
        "de:09162:1202",
        "de:09162:1203",
        "de:09162:1204",
        "de:09162:1205",
        "de:09162:1206",
        "de:09162:1208",
        "de:09162:1210",
        "de:09162:1211",
        "de:09162:1212",
        "de:09162:1213",
        "de:09162:1214",
        "de:09162:1215",
        "de:09162:1216",
        "de:09162:1217",
        "de:09162:1218",
        "de:09162:1220",
        "de:09162:1222",
        "de:09162:1224",
        "de:09162:1226",
        "de:09162:1230",
        "de:09162:1232",
        "de:09162:1234",
        "de:09162:1236",
        "de:09162:1240",
        "de:09162:1250",
        "de:09162:1260",
        "de:09162:1301",
        "de:09162:1302",
        "de:09162:1303",
        "de:09162:1304",
        "de:09162:1305",
        "de:09162:1306",
        "de:09162:1307",
        "de:09162:1308",
        "de:09162:1309",
        "de:09162:1310",
        "de:09162:1311",
        "de:09162:1312",
        "de:09162:1313",
        "de:09162:1315",
        "de:09162:1316",
        "de:09162:1317",
        "de:09162:1318",
        "de:09162:1319",
        "de:09162:1320",
        "de:09162:1321",
        "de:09162:1322",
        "de:09162:1323",
        "de:09162:1324",
        "de:09162:1325",
        "de:09162:1326",
        "de:09162:1327",
        "de:09162:1328",
        "de:09162:1329",
        "de:09162:1330",
        "de:09162:1331",
        "de:09162:1332",
        "de:09162:1333",
        "de:09162:1334",
        "de:09162:1335",
        "de:09162:1336",
        "de:09162:1337",
        "de:09162:1338",
        "de:09162:1339",
        "de:09162:1340",
        "de:09162:1341",
        "de:09162:1342",
        "de:09162:1344",
        "de:09162:1345",
        "de:09162:1346",
        "de:09162:1347",
        "de:09162:1349",
        "de:09162:1350",
        "de:09162:1351",
        "de:09162:1352",
        "de:09162:1353",
        "de:09162:1354",
        "de:09162:1355",
        "de:09162:1356",
        "de:09162:1357",
        "de:09162:1358",
        "de:09162:1359",
        "de:09162:1360",
        "de:09162:1361",
        "de:09162:1362",
        "de:09162:1402",
        "de:09162:1403",
        "de:09162:1404",
        "de:09162:1405",
        "de:09162:1408",
        "de:09162:1409",
        "de:09162:1411",
        "de:09162:1413",
        "de:09162:1415",
        "de:09162:1416",
        "de:09162:1421",
        "de:09162:1422",
        "de:09162:1423",
        "de:09162:1424",
        "de:09162:1426",
        "de:09162:1430",
        "de:09162:1431",
        "de:09162:1432",
        "de:09162:1434",
        "de:09162:1436",
        "de:09162:1437",
        "de:09162:1438",
        "de:09162:1440",
        "de:09162:1441",
        "de:09162:1442",
        "de:09162:1444",
        "de:09162:1446",
        "de:09162:1448",
        "de:09162:1450",
        "de:09162:1452",
        "de:09162:1454",
        "de:09162:1460",
        "de:09162:1462",
        "de:09162:1464",
        "de:09162:1466",
        "de:09162:1470",
        "de:09162:1472",
        "de:09162:1480",
        "de:09162:1490",
        "de:09162:1500",
        "de:09162:1502",
        "de:09162:1510",
        "de:09162:1514",
        "de:09162:1516",
        "de:09162:1518",
        "de:09162:1520",
        "de:09162:1524",
        "de:09162:1525",
        "de:09162:1526",
        "de:09162:1527",
        "de:09162:1530",
        "de:09162:1532",
        "de:09162:1533",
        "de:09162:1534",
        "de:09162:1535",
        "de:09162:1536",
        "de:09162:1537",
        "de:09162:1538",
        "de:09162:1540",
        "de:09162:1541",
        "de:09162:1542",
        "de:09162:1543",
        "de:09162:1544",
        "de:09162:1545",
        "de:09162:1546",
        "de:09162:1552",
        "de:09162:1554",
        "de:09162:1602",
        "de:09162:1604",
        "de:09162:1605",
        "de:09162:1606",
        "de:09162:1608",
        "de:09162:1612",
        "de:09162:1614",
        "de:09162:1618",
        "de:09162:1622",
        "de:09162:1623",
        "de:09162:1624",
        "de:09162:1626",
        "de:09162:1627",
        "de:09162:1628",
        "de:09162:1632",
        "de:09162:1633",
        "de:09162:1634",
        "de:09162:1636",
        "de:09162:1638",
        "de:09162:1643",
        "de:09162:1644",
        "de:09162:1646",
        "de:09162:1648",
        "de:09162:1652",
        "de:09162:1654",
        "de:09162:1656",
        "de:09162:1662",
        "de:09162:1664",
        "de:09162:1666",
        "de:09162:1668",
        "de:09162:1672",
        "de:09162:1674",
        "de:09162:1681",
        "de:09162:1682",
        "de:09162:1683",
        "de:09162:1701",
        "de:09162:1702",
        "de:09162:1704",
        "de:09162:1705",
        "de:09162:1706",
        "de:09162:1708",
        "de:09162:1710",
        "de:09162:1711",
        "de:09162:1712",
        "de:09162:1713",
        "de:09162:1715",
        "de:09162:1717",
        "de:09162:1718",
        "de:09162:1720",
        "de:09162:1721",
        "de:09162:1722",
        "de:09162:1724",
        "de:09162:1726",
        "de:09162:1727",
        "de:09162:1728",
        "de:09162:1732",
        "de:09162:1734",
        "de:09162:1735",
        "de:09162:1736",
        "de:09162:1737",
        "de:09162:1738",
        "de:09162:1739",
        "de:09162:1740",
        "de:09162:1741",
        "de:09162:1742",
        "de:09162:1743",
        "de:09162:1745",
        "de:09162:1746",
        "de:09162:1747",
        "de:09162:1748",
        "de:09162:1749",
        "de:09162:1750",
        "de:09162:1751",
        "de:09162:1753",
        "de:09162:1755",
        "de:09162:1756",
        "de:09162:1757",
        "de:09162:1758",
        "de:09162:1760",
        "de:09162:1762",
        "de:09162:1765",
        "de:09162:1766",
        "de:09162:1767",
        "de:09162:1768",
        "de:09162:1769",
        "de:09162:1770",
        "de:09162:1771",
        "de:09162:1772",
        "de:09162:1773",
        "de:09162:1774",
        "de:09162:1796",
        "de:09162:1797",
        "de:09162:1798",
        "de:09162:1799",
        "de:09162:1800",
        "de:09162:1801",
        "de:09162:1802",
        "de:09162:1803",
        "de:09162:1804",
        "de:09162:1805",
        "de:09162:1806",
        "de:09162:1807",
        "de:09162:1808",
        "de:09162:1809",
        "de:09162:1810",
        "de:09162:1811",
        "de:09162:1812",
        "de:09162:1814",
        "de:09162:1815",
        "de:09162:1816",
        "de:09162:1817",
        "de:09162:1818",
        "de:09162:1819",
        "de:09162:1820",
        "de:09162:1821",
        "de:09162:1822",
        "de:09162:1823",
        "de:09162:1825",
        "de:09162:1826",
        "de:09162:1828",
        "de:09162:1829",
        "de:09162:1830",
        "de:09162:1831",
        "de:09162:1832",
        "de:09162:1834",
        "de:09162:1835",
        "de:09162:1836",
        "de:09162:1837",
        "de:09162:1838",
        "de:09162:1839",
        "de:09162:1840",
        "de:09162:1841",
        "de:09162:1844",
        "de:09162:1846",
        "de:09162:1847",
        "de:09162:1848",
        "de:09162:1849",
        "de:09162:1850",
        "de:09162:1851",
        "de:09162:1852",
        "de:09162:1853",
        "de:09162:1854",
        "de:09162:1855",
        "de:09162:1856",
        "de:09162:1857",
        "de:09162:1858",
        "de:09162:1859",
        "de:09162:1860",
        "de:09162:1861",
        "de:09162:1863",
        "de:09162:1900",
        "de:09162:1901",
        "de:09162:1903",
        "de:09162:1904",
        "de:09162:1906",
        "de:09162:1908",
        "de:09162:1910",
        "de:09162:1911",
        "de:09162:1912",
        "de:09162:1914",
        "de:09162:1916",
        "de:09162:1918",
        "de:09162:1921",
        "de:09162:1924",
        "de:09162:1926",
        "de:09162:1928",
        "de:09162:1930",
        "de:09162:1931",
        "de:09162:1932",
        "de:09162:1934",
        "de:09162:1936",
        "de:09162:1938",
        "de:09162:1942",
        "de:09162:1943",
        "de:09162:1944",
        "de:09162:1945",
        "de:09162:1946",
        "de:09162:1948",
        "de:09162:1960",
        "de:09162:1961",
        "de:09162:1962",
        "de:09162:1963",
        "de:09162:1964",
        "de:09162:1965",
        "de:09162:1967",
        "de:09162:1968",
        "de:09162:1969",
        "de:09162:1973",
        "de:09162:1974",
        "de:09162:1975",
        "de:09162:1976",
        "de:09162:1978",
        "de:09162:1979",
        "de:09162:1981",
        "de:09162:1983",
        "de:09162:1984",
        "de:09162:1986",
        "de:09162:1987",
        "de:09184:2013",
        "de:09184:2030",
        "de:09184:2090",
        "de:09184:2092",
        "de:09184:2096",
        "de:09184:2098",
        "de:09184:2100",
        "de:09184:2101",
        "de:09184:2102",
        "de:09184:2107",
        "de:09184:2168",
        "de:09184:2169",
        "de:09184:2170",
        "de:09184:2172",
        "de:09184:2174",
        "de:09184:2176",
        "de:09184:2194",
        "de:09184:2265",
        "de:09184:2277",
        "de:09184:2287",
        "de:09184:2288",
        "de:09184:2292",
        "de:09184:2294",
        "de:09184:2296",
        "de:09184:2297",
        "de:09184:2298",
        "de:09184:2299",
        "de:09184:2359",
        "de:09184:2456",
        "de:09184:2458",
        "de:09184:2460",
        "de:09184:2462",
        "de:09184:2464",
        "de:09184:2490",
        "de:09184:2492",
        "de:09184:2493",
        "de:09175:3989",
        "de:09175:4310",
        "de:09162:5000",
        "de:09179:5799",
        "de:09179:5992",
        "de:09179:6103",
        "de:09179:6108",
        "de:09179:6111",
        "de:09179:6235",
        "de:09179:6250",
        "de:09179:6401",
        "de:09179:6448",
        "de:09179:6450",
        "de:09179:6452",
        "de:09179:6454",
        "de:09179:6455",
        "de:09179:6456",
        "de:09179:6457",
        "de:09179:6458",
        "de:09179:6462",
        "de:09179:6468",
        "de:09179:6471",
        "de:09179:6478",
        "de:09179:6479",
        "de:09179:6497",
        "de:09179:6499",
        "de:09179:6501",
        "de:09179:6606",
        "de:09174:6800",
        "de:09174:6874",
        "de:09174:6956",
        "de:09174:6968",
        "de:09174:6969",
        "de:09174:6970",
        "de:09174:6980",
        "de:09174:6982",
        "de:09174:6983",
        "de:09174:6984",
        "de:09174:6986",
        "de:09174:6988",
        "de:09174:6990",
        "de:09162:7000",
        "de:09174:7002",
        "de:09174:7052",
        "de:09174:7060",
        "de:09174:7061",
        "de:09174:7062",
        "de:09174:7066",
        "de:09174:7085",
        "de:09174:7391",
        "de:09174:7393",
        "de:09162:8019",
        "de:09162:8888",
        "de:09162:9015",
        "de:09162:9029",
    ]
    response = api.get_station_global_ids()
    assert isinstance(response, List)
    assert len(response) == len(station_ids)
    assert len(set(response).difference(set(station_ids))) == 0


def test_get_slim():
    api = Api()
    response = api.get_slim()
    assert isinstance(response, SlimList)


def test_get_route():
    api = Api()
    response = api.get_route(
        "de:09162:6",
        "de:09162:50",
        sap_tickets=True,
        _time=datetime.datetime.now(),
        transport_type_call_taxi=True,
        max_walk_time_to_dest=5,
        max_walk_time_to_start=5,
        change_limit=3,
    )
    assert isinstance(response, Connections)


def test_get_location():
    api = Api()
    response = api.get_location("Marienplatz")
    assert isinstance(response, LocationList)
    for location in response.locations:
        if location.type == LocationType.STATION:
            if location.name == "Marienplatz":
                return
    raise LocationNotFound("Loaction Marienplatz not foudn in LocationList")
