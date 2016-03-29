#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2016 Tom Samstag
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Unittest that tests person-specific filter rules
"""
import unittest

from gramps.gen.merge.diff import import_as_dict
from gramps.cli.user import User
from gramps.gen.filters import GenericFilter

from gramps.gen.filters.rules.person import *

class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = import_as_dict("example/gramps/example.gramps", User())

    def filter_with_rule(self, rule):
        filter_ = GenericFilter()
        filter_.add_rule(rule)
        results = filter_.apply(self.db)
        return set(results)

    def assert_rule_matches_ids(self, rule, ids):
        matching_handles = self.filter_with_rule(rule)
        matching_ids = [self.db.get_person_from_handle(handle).get_gramps_id()
                for handle in matching_handles]
        self.assertEqual(set(matching_ids), set(ids))

    def assert_rule_matches_count(self, rule, count):
        matching_handles = self.filter_with_rule(rule)
        self.assertEqual(len(matching_handles), count)

    def test_Disconnected(self):
        rule = Disconnected([])
        self.assert_rule_matches_ids(rule, [
            'I0461', 'I0506', 'I0282', 'I0400', 'I1177', 'I1341', 'I0393',
            'I0210', 'I0382', 'I1143', 'I0634', 'I1130', 'I0937', 'I0389',
            'I1017', 'I0886', 'I0392', 'I0401', 'I0891', 'I0783', 'I0534',
            'I0206', 'I1059', 'I0402', 'I0398', 'I0284', 'I0503', 'I1340',
            'I0076', 'I0884', 'I1342', 'I0697', 'I0175', 'I0922', 'I1026',
            'I0391', 'I0743', 'I0399', 'I0883', 'I0810', 'I0283', 'I1337',
            'I0843', 'I0381', 'I0386', 'I0694', 'I2116', 'I0396', 'I1025',
            'I0924', 'I0384', 'I0885', 'I0782', 'I0630', 'I0397', 'I0923',
            'I0385', 'I0877', 'I0913', 'I0736', 'I1792', 'I0388', 'I0243',
            'I1338', 'I1104', 'I0460', 'I0383', 'I0387', 'I0570', 'I0688',
            'I0998', 'I0912',
            ])

    def test_Everyone(self):
        rule = Everyone([])
        self.assert_rule_matches_count(rule, self.db.get_number_of_people())

    def test_FamilyWithIncompleteEvent(self):
        rule = FamilyWithIncompleteEvent([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 775)

    def test_HasAlternateName(self):
        rule = HasAlternateName([])
        self.assert_rule_matches_ids(rule, [
            'I0044', 'I0107',
            ])

    def test_HasCommonAncestorWith_empty(self):
        rule = HasCommonAncestorWith([''])
        self.assert_rule_matches_count(rule, 0)

    def test_HasCommonAncestorWith_nonmatching(self):
        rule = HasCommonAncestorWith(['I0000'])
        self.assert_rule_matches_count(rule, 0)

    def test_HasCommonAncestorWith_irregular(self):
        rule = HasCommonAncestorWith(['ABCDEFG'])
        self.assert_rule_matches_count(rule, 0)

    def test_HasCommonAncestorWith_matching(self):
        rule = HasCommonAncestorWith(['I0044'])
        self.assert_rule_matches_ids(rule, [
            'I1105', 'I0648', 'I0003', 'I1126', 'I0001', 'I0120', 'I1335',
            'I1053', 'I1123', 'I0004', 'I0642', 'I0121', 'I0658', 'I0657',
            'I0624', 'I0136', 'I1050', 'I1062', 'I1039', 'I0182', 'I1065',
            'I0625', 'I1117', 'I0010', 'I0006', 'I0046', 'I1043', 'I0178',
            'I0016', 'I0176', 'I0627', 'I0186', 'I1106', 'I0017', 'I1048',
            'I0015', 'I1068', 'I0044', 'I1112', 'I1047', 'I0183', 'I0106',
            'I1064', 'I0647', 'I0972', 'I0105', 'I1121', 'I2044', 'I1045',
            'I0626', 'I1069', 'I0107', 'I1115', 'I0002', 'I1061', 'I0623',
            'I1113', 'I0009', 'I0644', 'I0019', 'I1125', 'I1119', 'I0179',
            'I0125', 'I1046', 'I0119', 'I0177', 'I0651', 'I0653', 'I1128',
            'I1108', 'I0185', 'I1052', 'I0629', 'I0018', 'I0655', 'I0184',
            'I1060', 'I1055', 'I1067', 'I0180', 'I1114', 'I0973', 'I0646',
            'I1110', 'I0181', 'I0628', 'I1111', 'I1041', 'I1116', 'I0124',
            'I1056', 'I0135', 'I0656', 'I0122', 'I1109', 'I0104',
            ])

    def test_HasNickname(self):
        rule = HasNickname([])
        self.assert_rule_matches_ids(rule, [
            'I0044', 'I1200', 'I2108',
            ])

    def test_HasUnknownGender(self):
        rule = HasUnknownGender([])
        self.assert_rule_matches_ids(rule, [
            'I1338', 'I2067', 'I1586', 'I2055', 'I1099', 'I1509', 'I1206',
            'I1639', 'I1205', 'I1111', 'I2054', 'I1590', 'I1101', 'I2013',
            'I2068', 'I1587', 'I1337', 'I1100', 'I1271', 'I2053',
            ])

    def test_HasSourceOf_empty(self):
        # this rule run with an empty string finds people with no source citations
        rule = HasSourceOf([''])
        self.assert_rule_matches_ids(rule, [
            'I2110', 'I2106', 'I2114', 'I2109', 'I2113', 'I2115', 'I2111',
            'I2105', 'I2116', 'I2112', 'I2107', 'I2108',
            ])

    def test_HasSourceOf_nonmatching(self):
        rule = HasSourceOf(['S0004'])
        self.assert_rule_matches_count(rule, 0)

    def test_HasSourceOf_irregular(self):
        rule = HasSourceOf(['ABCDEFG'])
        self.assert_rule_matches_count(rule, 0)

    def test_HasSourceOf_matching(self):
        rule = HasSourceOf(['S0000'])
        self.assert_rule_matches_ids(rule, [
            'I0044',
            ])

    def test_HaveAltFamilies(self):
        rule = HaveAltFamilies([])
        self.assert_rule_matches_ids(rule, [
            'I0625', 'I0624',
            ])

    def test_HaveChildren(self):
        rule = HaveChildren([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 895)

    def test_IncompleteNames(self):
        rule = IncompleteNames([])
        self.assert_rule_matches_ids(rule, [
            'I1066', 'I2039', 'I1871', 'I1338', 'I2075', 'I1450', 'I2037',
            'I2067', 'I1541', 'I2045', 'I2110', 'I2072', 'I1832', 'I1474',
            'I1834', 'I1042', 'I1383', 'I1814', 'I1816', 'I0992', 'I1586',
            'I2115', 'I0458', 'I1813', 'I1738', 'I2047', 'I2073', 'I2065',
            'I1836', 'I1709', 'I2113', 'I1867', 'I1587', 'I1337', 'I2114',
            'I2109', 'I1437', 'I1828', 'I1844', 'I1195', 'I2107', 'I1878',
            'I2003', 'I1112', 'I2111', 'I2106', 'I2074', 'I2105', 'I1737',
            'I1271', 'I2090', 'I1883', 'I1116', 'I1837', 'I1417', 'I2046',
            'I1838', 'I1815', 'I2103', 'I1509', 'I2043', 'I2108', 'I1925',
            'I2055', 'I1447', 'I2053', 'I1826', 'I2068', 'I1830', 'I1824',
            'I1422', 'I2023', 'I1853', 'I2054', 'I1856', 'I2076',
            ])

    def test_IsBookmarked(self):
        rule = IsBookmarked([])
        self.assert_rule_matches_ids(rule, [
            'I0106', 'I1123', 'I1200',
            ])

    def test_IsDuplicatedAncestorOf_empty(self):
        rule = IsDuplicatedAncestorOf([''])
        self.assert_rule_matches_count(rule, 0)

    def test_IsDuplicatedAncestorOf_nonmatching(self):
        rule = IsDuplicatedAncestorOf(['I0000'])
        self.assert_rule_matches_count(rule, 0)

    def test_IsDuplicatedAncestorOf_irregular(self):
        rule = IsDuplicatedAncestorOf(['ABCDEFG'])
        self.assert_rule_matches_count(rule, 0)

    def test_IsDuplicatedAncestorOf_matching(self):
        rule = IsDuplicatedAncestorOf(['I1631'])
        self.assert_rule_matches_ids(rule, [
            'I0063', 'I0062',
            ])

    def test_IsRelatedWith_empty(self):
        rule = IsRelatedWith([''])
        self.assert_rule_matches_count(rule, 0)

    def test_IsRelatedWith_nonmatching(self):
        rule = IsRelatedWith(['I0000'])
        self.assert_rule_matches_count(rule, 0)

    def test_IsRelatedWith_irregular(self):
        rule = IsRelatedWith(['ABCDEFG'])
        self.assert_rule_matches_count(rule, 0)

    def test_IsRelatedWith_matching(self):
        rule = IsRelatedWith(['I1844'])
        self.assert_rule_matches_ids(rule, [
            'I1800', 'I1809', 'I1795', 'I1843', 'I1810', 'I1797', 'I1829',
            'I1815', 'I1819', 'I1822', 'I1825', 'I1835', 'I1824', 'I1811',
            'I1844', 'I1813', 'I1821', 'I1842', 'I1820', 'I1798', 'I1831',
            'I1796', 'I1830', 'I1836', 'I1826', 'I1823', 'I1839', 'I1793',
            'I1802', 'I1840', 'I1808', 'I1837', 'I1804', 'I1814', 'I1801',
            'I1838', 'I1834', 'I1832', 'I1841', 'I1794', 'I1799', 'I1806',
            'I1803', 'I1816', 'I1817', 'I1828', 'I1827', 'I1791', 'I1807',
            'I1805', 'I1833', 'I1818', 'I1812',
            ])

    def test_HasIdOf_empty(self):
        rule = HasIdOf([''])
        self.assert_rule_matches_count(rule, 0)

    def test_HasIdOf_nonmatching(self):
        rule = HasIdOf(['I0000'])
        self.assert_rule_matches_count(rule, 0)

    def test_HasIdOf_irregular(self):
        rule = HasIdOf(['ABCDEFG'])
        self.assert_rule_matches_count(rule, 0)

    def test_HasIdOf_matching(self):
        rule = HasIdOf(['I0044'])
        self.assert_rule_matches_ids(rule, [
            'I0044',
            ])

    def test_IsDefaultPerson(self):
        rule = IsDefaultPerson([])
        self.assert_rule_matches_ids(rule, [
            'I0044',
            ])

    def test_IsFemale(self):
        rule = IsFemale([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 928)

    def test_IsMale(self):
        rule = IsMale([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 1154)

    def test_MissingParent(self):
        rule = MissingParent([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 849)

    def test_MultipleMarriages(self):
        rule = MultipleMarriages([])
        self.assert_rule_matches_ids(rule, [
            'I1548', 'I0236', 'I0053', 'I0525', 'I0577', 'I0575', 'I1894',
            'I0232', 'I0135', 'I0027', 'I0855', 'I1015', 'I2034', 'I0573',
            'I1197', 'I0154', 'I0888', 'I1406', 'I0476', 'I0105', 'I0228',
            'I0471', 'I0457', 'I0241', 'I0574', 'I0715', 'I1167', 'I1547',
            'I0438', 'I0984', 'I1725', 'I1023', 'I2111', 'I0532', 'I1545',
            'I2110', 'I1557', 'I0163', 'I2002', 'I0245', 'I0368', 'I0047',
            'I0020', 'I0097', 'I0257', 'I0094', 'I0130', 'I0750', 'I0183',
            'I1355',
            ])

    def test_NeverMarried(self):
        rule = NeverMarried([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 749)

    def test_NoBirthdate(self):
        rule = NoBirthdate([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 966)

    def test_NoDeathdate(self):
        rule = NoDeathdate([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 1581)

    def test_PeoplePrivate(self):
        # TODO: example.gramps has no people marked private
        rule = PeoplePrivate([])
        self.assert_rule_matches_count(rule, 0)

    def test_PeoplePublic(self):
        rule = PeoplePublic([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 2102)

    def test_PersonWithIncompleteEvent(self):
        rule = PersonWithIncompleteEvent([])
        # too many to list out to test explicitly
        self.assert_rule_matches_count(rule, 740)

    def test_RelationshipPathBetweenBookmarks(self):
        rule = RelationshipPathBetweenBookmarks([])
        self.assert_rule_matches_ids(rule, [
            'I0105', 'I0106', 'I0104', 'I1123', 'I1200',
            ])


if __name__ == "__main__":
    unittest.main()
