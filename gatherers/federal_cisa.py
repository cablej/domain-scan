import os
import logging

import requests

from gatherers.gathererabc import Gatherer
from utils import utils

# Gathers federal hostnames that are subject to CISA's scanning
class Gatherer(Gatherer):

    def gather(self):
        # Fetch GSA domains
        remote_path = os.path.join(self.cache_dir, "url.csv")

        try:
            response = requests.get("https://raw.githubusercontent.com/GSA/data/master/dotgov-domains/current-federal.csv")
            utils.write(response.text, remote_path)
        except:
            logging.error("Remote URL not downloaded successfully.")
            print(utils.format_last_exception())
            exit(1)

        for domain in utils.load_domains(remote_path, whole_rows=True):
            # Check that agency is executive and is under CISA's purview
            # if domain[1] == "Federal Agency - Executive" and (domain[2] in all_cisa_orgs or domain[3] in all_cisa_orgs):
            if domain[1] == "Federal Agency - Executive":
                yield domain[0]

# List of all organizations that are under CISA's purview, from https://cyber.dhs.gov/agencies/
# As this list is infrequently updated and contains slight formatting differences, we maintain it as an array here
all_cisa_orgs = set(["Administrative Conference of the United States", "Advisory Council on Historic Preservation", "African Development Foundation", "American Battle Monuments Commission", "Armed Forces Retirement Home", "Barry Goldwater Scholarship and Excellence in Education Foundation", "Board of Governors of the Federal Reserve", "Chemical Safety Board", "Commission of Fine Arts", "Commodity Futures Trading Commission", "Consumer Financial Protection Bureau", "Consumer Product Safety Commission", "Corporation for National and Community Service", "Council of the Inspectors General on Integrity and Efficiency", "Court Services and Offender Supervision Agency", "Defense Nuclear Facilities Safety Board", "Denali Commission", "Department of Commerce", "Department of Education", "Department of Energy", "Department of Health and Human Services", "Department of Homeland Security", "Department of Housing and Urban Development", "Department of Justice", "Department of Labor", "Department of State", "Department of the Interior", "Department of the Treasury", "Department of Transportation", "Department of Veterans Affairs", "Election Assistance Commission", "Environmental Protection Agency", "Equal Employment Opportunity Commission", "Export-Import Bank of the United States", "Farm Credit Administration", "Farm Credit System Insurance Corporation", "Federal Communications Commission", "Federal Deposit Insurance Corporation", "Federal Energy Regulatory Commission", "Federal Housing Finance Agency", "Federal Labor Relations Authority", "Federal Maritime Commission", "Federal Mediation and Conciliation Service", "Federal Mine Safety and Health Review Commission", "Federal Retirement Thrift Investment Board", "Federal Trade Commission", "General Services Administration", "Gulf Coast Ecosystem Restoration Council", "Harry S Truman Scholarship Foundation", "Institute of Museum and Library Services", "Inter-American Foundation", "James Madison Memorial Fellowship Foundation", "Japan-United States Friendship Commission", "Marine Mammal Commission", "Merit Systems Protection Board", "Millennium Challenge Corporation", "Morris K. Udall and Stewart L. Udall Foundation", "National Aeronautics and Space Administration", "National Archives and Records Administration", "National Capital Planning Commission", "National Commission on Military, National, and Public Service ", "National Council on Disability", "National Credit Union Administration", "National Endowment for the Arts", "National Endowment for the Humanities", "National Labor Relations Board", "National Mediation Board", "National Science Foundation", "National Transportation Safety Board", "Nuclear Regulatory Commission", "Nuclear Waste Technical Review Board", "Occupational Safety and Health Review Commission", "Office of the Comptroller of the Currency", "Office of Government Ethics", "Office of Navajo and Hopi Indian Relocation", "Office of Personnel Management", "Office of Special Counsel", "Peace Corps", "Pension Benefit Guaranty Corporation", "Postal Regulatory Commission", "Presidio Trust", "Privacy and Civil Liberties Oversight Board", "Railroad Retirement Board", "Securities and Exchange Commission", "Selective Service System", "Small Business Administration", "Social Security Administration", "Social Security Advisory Board", "Surface Transportation Board", "Tennessee Valley Authority", "International Boundary and Water Commission", "United States AbilityOne Commission", "United States Access Board", "United States Agency for Global Media", "United States Agency for International Development", "United States Commission on Civil Rights", "United States Department of Agriculture", "United States Interagency Council on Homelessness", "United States International Development Finance Corporation", "United States International Trade Commission", "United States Trade and Development Agency"])
