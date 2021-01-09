import pytest
from context import src
import src.uhc_reports_rename as rename
#import uhc_reports_rename as rename


@pytest.mark.parametrize("test_input,expected", [
    ("B6744PRD_RPT_202003_015_015_001_EC7280_A01_000000363.PDF",
     "2020/Medica/202003_member_changes_cap_details_Medica.pdf"),
    ("B6744PRD_RPT_202003_016_016_001_EC7280_A01_000000363.PDF",
     "2020/PCP/202003_member_changes_cap_details_PCP.pdf"),

    ("B6744PRD_RPT_202004_015_015_001_EC7010_A02_000000503.PDF",
     "2020/Medica/202004_cap_paid_recap_details_Medica.pdf"),
    ("B6744PRD_RPT_202004_016_016_001_EC7010_A02_000000503.PDF",
     "2020/PCP/202004_cap_paid_recap_details_PCP.pdf"),

    ("B6744PRD_RPT_202004_015_015_001_EC7250_A01_000000346.PDF",
     "2020/Medica/202004_cap_details_Medica.pdf"),
    ("B6744PRD_RPT_202004_016_016_001_EC7250_A01_000000346.PDF",
     "2020/PCP/202004_cap_details_PCP.pdf"),

    ("B6744PRD_RPT_202011_015_015_001_EC7090_A02_000000856.PDF",
     "2020/Medica/202011_member_changes_cap_summary_Medica.pdf"),
    ("B6744PRD_RPT_202011_016_016_001_EC7090_A02_000000856.PDF",
     "2020/PCP/202011_member_changes_cap_summary_PCP.pdf"),

    ("B6744PRD_RPT_202004_017_017_001_EC7999_A01_000000346.PDF",
     "2020/WRONG-PAYER-17/202004_WRONG-REPORTTYPE-7999_A01_WRONG-PAYER-17.pdf"),
])
def test_pdf_rename(test_input, expected):
    new_name = rename.pdf_name_converter(test_input)
    print(new_name)
    assert new_name == expected


@pytest.mark.parametrize("test_input,", [
    ("B6744PRD_RPT_YYYYMM_015_015_001_EC7010_A02_000000503.PDF"),
    ("B6744PRD_RPT_202004_DDD_015_001_EC7010_A02_000000503.PDF"),
])
def test_pdf_rename_exception(test_input):
    with pytest.raises(ValueError):
        rename.pdf_name_converter(test_input)


@pytest.mark.parametrize("test_input,expected", [
    ("B6744PRD.P202001.S015.M015001.E7810.S0000123.csv",
     "2020/Medica/202001_spreadsheet_Medica.csv"),
    ("B6744PRD.P202001.S016.M016001.E7810.S0000123.csv",
     "2020/PCP/202001_spreadsheet_PCP.csv"),
])
def test_csv_rename(test_input, expected):
    new_name = rename.csv_name_converter(test_input)
    print(new_name)
    assert new_name == expected


@pytest.mark.parametrize("test_input,", [
    ("B6744PRD.PYYYYMM.S015.M015001.E7810.S0000123.csv"),
    ("B6744PRD.P202001.SDDD.M016001.E7810.S0000123.csv"),
])
def test_csv_rename_exception(test_input):
    with pytest.raises(ValueError):
        rename.csv_name_converter(test_input)


def test_add():
    value = 2.0 + 4.0
    assert value == 6.0
