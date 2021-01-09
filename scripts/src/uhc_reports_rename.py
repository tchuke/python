# uhc_reports_rename.py

import re
import os
from zipfile import ZipFile

# Style 1 (spreadsheets)
# UHMHPMR_202001_EC7810_003029286_000000000_000000000_CDF_0000094.ZIP"
# B6744PRD.P202001.S015.M015001.E7810.S0000094.csv
# UHPCPMR_202001_EC7810_003029286_000000000_000000000_CDF_0000123.ZIP
# B6744PRD.P202001.S016.M016001.E7810.S0000123.csv
#                       ----
# Style 2 (PDFs)
# UHMHPMR_202003_EC7280A01_003029286_003029286_000000000_RPT_000000363.ZIP
# B6744PRD_RPT_202003_015_015_001_EC7280_A01_000000363.PDF
# UHMHPMR_202004_EC7010A02_003029286_003029286_000000000_RPT_000000846.ZIP
# B6744PRD_RPT_202004_015_015_001_EC7010_A02_000000846.PDF
# UHMHPMR_202004_EC7250A01_003029286_003029286_000000000_RPT_000000346.ZIP
# B6744PRD_RPT_202004_015_015_001_EC7250_A01_000000346.PDF
# UHPCPMR_202011_EC7090A02_003029286_003029286_000000000_RPT_000000856.ZIP
# B6744PRD_RPT_202011_016_016_001_EC7090_A02_000000856.PDF


def id_to_payer(payer_id):
    switcher = {
        "15": "Medica",
        "16": "PCP"
    }
    return switcher.get(payer_id, "WRONG-PAYER-" + payer_id)


def id_to_report_type(report_id):
    switcher = {
        "7250_A01": "cap_details",  # one flavor
        "7010_A02": "cap_paid_recap_details",  # details rather than summary flavor
        "7280_A01": "member_changes_cap_details",  # one flavor
        "7090_A02": "member_changes_cap_summary",  # details rather than summary flavor
    }
    return switcher.get(report_id, "WRONG-REPORTTYPE-" + report_id)


def csv_name_converter(name):
   # B6744PRD.P202001.S016.M016001.E7810.S0000123.csv
    pattern = re.compile(r'\w+\.P(\d{4})(\d{2})\.S0(\d{2})\.\S+')
    matcher = pattern.match(name)
    if matcher:
        yyyy = matcher.group(1)
        mm = matcher.group(2)
        payer_id = matcher.group(3)
        payer_name = id_to_payer(payer_id)
        new_name = f'{yyyy}/{payer_name}/{yyyy}{mm}_spreadsheet_{payer_name}.csv'
        return new_name
    else:
        raise ValueError("Doesn't match: " + name)


def pdf_name_converter(name):
    # B6744PRD_RPT_202003_015_015_001_EC7280_A01_000000363.PDF
    pattern = re.compile(
        r'\w+_RPT_(\d{4})(\d{2})_0(\d\d)_\S+_EC(\d{4}_A\d{2})_\S+')
    matcher = pattern.match(name)
    # print("match? " + str(matcher))
    if matcher:
        yyyy = matcher.group(1)
        mm = matcher.group(2)
        payer_id = matcher.group(3)
        report_type_id = matcher.group(4)
        payer_name = id_to_payer(payer_id)
        report_name = id_to_report_type(report_type_id)
        new_name = f'{yyyy}/{payer_name}/{yyyy}{mm}_{report_name}_{payer_name}.pdf'
        return new_name
    else:
        raise ValueError("Doesn't match: " + name)


def extractAndRenameAllZipsCurrentDirectory():
    source_dir = os.getcwd()
    source_dir_name = os.path.basename(source_dir)
    target_dir = f'../output-{source_dir_name}/'
    print(
        f'Extracting zips from this directory, {source_dir_name}, to {target_dir}')

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in [f for f in os.listdir(source_dir)]:
        full_path = f'{source_dir}/{filename}'
        if os.path.isfile(full_path):
            print(f'Found a zip: {filename}')
            with ZipFile(full_path) as z:
                z.printdir()
                z.extractall(target_dir)

    for filename in os.listdir(target_dir):
        __, extension = os.path.splitext(filename)
        extension_lower = extension.lower()
        print("Extension is " + extension)
        if extension_lower == ".csv":
            new_filename = csv_name_converter(filename)
        elif extension_lower == ".pdf":
            new_filename = pdf_name_converter(filename)
        else:
            new_filename = filename

        print("new filename is: " + new_filename)
        [dest_dir, __] = new_filename.rsplit('/', 1)
        full_target_dir = f'{target_dir}/{dest_dir}'
        if os.path.isdir(full_target_dir) == False:
            os.makedirs(full_target_dir)

        os.rename(f'{target_dir}/{filename}', f'{target_dir}/{new_filename}')


def main():
    extractAndRenameAllZipsCurrentDirectory()


if __name__ == '__main__':
    main()
