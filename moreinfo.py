#! /usr/bin/env python

from beets.plugins import BeetsPlugin
from beets.ui import Subcommand

def print_table(lib, opts,args):
    results = lib.items(u":.")
    era_dict = {}
    genre_dict = {}
    country_dict = {}
    count = 0
    ISO3166 = get_code_dict()
    for row in results.rows:
        count += 1
        d = dict(row)
        code = d['country']
        if code in ISO3166:
            country = ISO3166[d['country']]
        else:
            country = ""
        if country not in country_dict:
            country_dict[country] = 1
        else:
            country_dict[country] += 1
        if "year" in d.keys():
            date = d["year"]
            mil = date // 100
            dec = (date) // 10 * 10
            if mil < 19:
                if "pre-1900" in era_dict:
                    era_dict["pre-1900"] += 1
                else:
                    era_dict["pre-1900"] = 1
            else:
                if dec in era_dict:
                    era_dict[dec] += 1
                else:
                    era_dict[dec] = 1
        else:
            if "unknown" in era_dict:
                era_dict["unknown"] += 1
            else:
                era_dict["unknown"] = 1
        for genre in d['genre'].split(", "):
            if genre not in genre_dict:
                genre_dict[genre] = 1
            else:
                genre_dict[genre] += 1

    zipped = zip(get_top_10(genre_dict), get_top_10(country_dict), get_top_10(era_dict))

    #[print(x[0]) for x in list(zipped)]
    print("_","_"*30,"_","_"*30,"_","_"*15,"_","_"*6,sep="")
    print("|","TOP 10 GENRES".ljust(30),"|","TOP 10 COUNTRIES".ljust(30),"|","TOP DECADES".ljust(15),"|")
    print("|","_"*30,"|","_"*30,"|","_"*15,"|")
    [print("|",x[0].ljust(30), "|",x[1][:30].ljust(30),"|",x[2].ljust(15),"|") for x in list(zipped)]
    print("_","_"*30,"_","_"*30,"_","_"*15,"_","_"*6,sep="")
    return

def get_top_10(d):
    res = []
    count = 0
    for key in sorted(d, key=lambda x : d[x],reverse=True):
        res.append(str(key)+" ("+str(d[key])+")")
        count += 1
        if count > 9:
            return res
    res += ["" for _ in range(10-count)]
    return res

def get_code_dict():
    ISO3166 = {
            ''  : 'Worldwide [unknown]',
            'XE': 'Europe',
            'SU': 'Soviet Union',
            'XW': 'Worldwide [unknown]',
            'AD': 'Andorra',
            'AE': 'United Arab Emirates',
            'AF': 'Afghanistan',
            'AG': 'Antigua & Barbuda',
            'AI': 'Anguilla',
            'AL': 'Albania',
            'AM': 'Armenia',
            'AN': 'Netherlands Antilles',
            'AO': 'Angola',
            'AQ': 'Antarctica',
            'AR': 'Argentina',
            'AS': 'American Samoa',
            'AT': 'Austria',
            'AU': 'Australia',
            'AW': 'Aruba',
            'AZ': 'Azerbaijan',
            'BA': 'Bosnia and Herzegovina',
            'BB': 'Barbados',
            'BD': 'Bangladesh',
            'BE': 'Belgium',
            'BF': 'Burkina Faso',
            'BG': 'Bulgaria',
            'BH': 'Bahrain',
            'BI': 'Burundi',
            'BJ': 'Benin',
            'BM': 'Bermuda',
            'BN': 'Brunei Darussalam',
            'BO': 'Bolivia',
            'BR': 'Brazil',
            'BS': 'Bahama',
            'BT': 'Bhutan',
            'BU': 'Burma (no longer exists)',
            'BV': 'Bouvet Island',
            'BW': 'Botswana',
            'BY': 'Belarus',
            'BZ': 'Belize',
            'CA': 'Canada',
            'CC': 'Cocos (Keeling) Islands',
            'CF': 'Central African Republic',
            'CG': 'Congo',
            'CH': 'Switzerland',
            'CI': 'Côte D\'ivoire (Ivory Coast)',
            'CK': 'Cook Iislands',
            'CL': 'Chile',
            'CM': 'Cameroon',
            'CN': 'China',
            'CO': 'Colombia',
            'CR': 'Costa Rica',
            'CS': 'Czechoslovakia (no longer exists)',
            'CU': 'Cuba',
            'CV': 'Cape Verde',
            'CX': 'Christmas Island',
            'CY': 'Cyprus',
            'CZ': 'Czech Republic',
            'DD': 'German Democratic Republic (no longer exists)',
            'DE': 'Germany',
            'DJ': 'Djibouti',
            'DK': 'Denmark',
            'DM': 'Dominica',
            'DO': 'Dominican Republic',
            'DZ': 'Algeria',
            'EC': 'Ecuador',
            'EE': 'Estonia',
            'EG': 'Egypt',
            'EH': 'Western Sahara',
            'ER': 'Eritrea',
            'ES': 'Spain',
            'ET': 'Ethiopia',
            'FI': 'Finland',
            'FJ': 'Fiji',
            'FK': 'Falkland Islands (Malvinas)',
            'FM': 'Micronesia',
            'FO': 'Faroe Islands',
            'FR': 'France',
            'FX': 'France, Metropolitan',
            'GA': 'Gabon',
            'GB': 'United Kingdom',
            'GD': 'Grenada',
            'GE': 'Georgia',
            'GF': 'French Guiana',
            'GH': 'Ghana',
            'GI': 'Gibraltar',
            'GL': 'Greenland',
            'GM': 'Gambia',
            'GN': 'Guinea',
            'GP': 'Guadeloupe',
            'GQ': 'Equatorial Guinea',
            'GR': 'Greece',
            'GS': 'South Georgia and the South Sandwich Islands',
            'GT': 'Guatemala',
            'GU': 'Guam',
            'GW': 'Guinea-Bissau',
            'GY': 'Guyana',
            'HK': 'Hong Kong',
            'HM': 'Heard & McDonald Islands',
            'HN': 'Honduras',
            'HR': 'Croatia',
            'HT': 'Haiti',
            'HU': 'Hungary',
            'ID': 'Indonesia',
            'IE': 'Ireland',
            'IL': 'Israel',
            'IN': 'India',
            'IO': 'British Indian Ocean Territory',
            'IQ': 'Iraq',
            'IR': 'Islamic Republic of Iran',
            'IS': 'Iceland',
            'IT': 'Italy',
            'JM': 'Jamaica',
            'JO': 'Jordan',
            'JP': 'Japan',
            'KE': 'Kenya',
            'KG': 'Kyrgyzstan',
            'KH': 'Cambodia',
            'KI': 'Kiribati',
            'KM': 'Comoros',
            'KN': 'St. Kitts and Nevis',
            'KP': 'Korea, Democratic People\'s Republic of',
            'KR': 'Korea, Republic of',
            'KW': 'Kuwait',
            'KY': 'Cayman Islands',
            'KZ': 'Kazakhstan',
            'LA': 'Lao People\'s Democratic Republic',
            'LB': 'Lebanon',
            'LC': 'Saint Lucia',
            'LI': 'Liechtenstein',
            'LK': 'Sri Lanka',
            'LR': 'Liberia',
            'LS': 'Lesotho',
            'LT': 'Lithuania',
            'LU': 'Luxembourg',
            'LV': 'Latvia',
            'LY': 'Libyan Arab Jamahiriya',
            'MA': 'Morocco',
            'MC': 'Monaco',
            'MD': 'Moldova, Republic of',
            'MG': 'Madagascar',
            'MH': 'Marshall Islands',
            'ML': 'Mali',
            'MN': 'Mongolia',
            'MM': 'Myanmar',
            'MO': 'Macau',
            'MP': 'Northern Mariana Islands',
            'MQ': 'Martinique',
            'MR': 'Mauritania',
            'MS': 'Monserrat',
            'MT': 'Malta',
            'MU': 'Mauritius',
            'MV': 'Maldives',
            'MW': 'Malawi',
            'MX': 'Mexico',
            'MY': 'Malaysia',
            'MZ': 'Mozambique',
            'NA': 'Namibia',
            'NC': 'New Caledonia',
            'NE': 'Niger',
            'NF': 'Norfolk Island',
            'NG': 'Nigeria',
            'NI': 'Nicaragua',
            'NL': 'Netherlands',
            'NO': 'Norway',
            'NP': 'Nepal',
            'NR': 'Nauru',
            'NT': 'Neutral Zone (no longer exists)',
            'NU': 'Niue',
            'NZ': 'New Zealand',
            'OM': 'Oman',
            'PA': 'Panama',
            'PE': 'Peru',
            'PF': 'French Polynesia',
            'PG': 'Papua New Guinea',
            'PH': 'Philippines',
            'PK': 'Pakistan',
            'PL': 'Poland',
            'PM': 'St. Pierre & Miquelon',
            'PN': 'Pitcairn',
            'PR': 'Puerto Rico',
            'PT': 'Portugal',
            'PW': 'Palau',
            'PY': 'Paraguay',
            'QA': 'Qatar',
            'RE': 'Réunion',
            'RO': 'Romania',
            'RU': 'Russian Federation',
            'RW': 'Rwanda',
            'SA': 'Saudi Arabia',
            'SB': 'Solomon Islands',
            'SC': 'Seychelles',
            'SD': 'Sudan',
            'SE': 'Sweden',
            'SG': 'Singapore',
            'SH': 'St. Helena',
            'SI': 'Slovenia',
            'SJ': 'Svalbard & Jan Mayen Islands',
            'SK': 'Slovakia',
            'SL': 'Sierra Leone',
            'SM': 'San Marino',
            'SN': 'Senegal',
            'SO': 'Somalia',
            'SR': 'Suriname',
            'ST': 'Sao Tome & Principe',
            'SU': 'Union of Soviet Socialist Republics (no longer exists)',
            'SV': 'El Salvador',
            'SY': 'Syrian Arab Republic',
            'SZ': 'Swaziland',
            'TC': 'Turks & Caicos Islands',
            'TD': 'Chad',
            'TF': 'French Southern Territories',
            'TG': 'Togo',
            'TH': 'Thailand',
            'TJ': 'Tajikistan',
            'TK': 'Tokelau',
            'TM': 'Turkmenistan',
            'TN': 'Tunisia',
            'TO': 'Tonga',
            'TP': 'East Timor',
            'TR': 'Turkey',
            'TT': 'Trinidad & Tobago',
            'TV': 'Tuvalu',
            'TW': 'Taiwan',
            'TZ': 'Tanzania, United Republic of',
            'UA': 'Ukraine',
            'UG': 'Uganda',
            'UM': 'United States Minor Outlying Islands',
            'US': 'United States of America',
            'UY': 'Uruguay',
            'UZ': 'Uzbekistan',
            'VA': 'Vatican City State (Holy See)',
            'VC': 'St. Vincent & the Grenadines',
            'VE': 'Venezuela',
            'VG': 'British Virgin Islands',
            'VI': 'United States Virgin Islands',
            'VN': 'Viet Nam',
            'VU': 'Vanuatu',
            'WF': 'Wallis & Futuna Islands',
            'WS': 'Samoa',
            'YD': 'Democratic Yemen (no longer exists)',
            'YE': 'Yemen',
            'YT': 'Mayotte',
            'YU': 'Yugoslavia',
            'ZA': 'South Africa',
            'ZM': 'Zambia',
            'ZR': 'Zaire',
            'ZW': 'Zimbabwe',
            'ZZ': 'Unknown or unspecified country',
    }
    return ISO3166

print_command = Subcommand("moreinfo", help="Print more verbose library summary")
print_command.func = print_table

class MoreInfo(BeetsPlugin):
    def commands(self):
        return [print_command]
