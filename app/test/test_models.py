##
# Tests database models by populating data and testing functions accessing that
# data. 
# 
# To make a test, make sure all methods begin with test_
#
# @author eir; Erik W. Greif
# @date   2016.02.19
##

from app.models import User
import unittest

class TestModels(unittest.TestCase):

    # Set up basic user for testing
    def setUp(self):
        self.u = User(email="tom@test.com", username="tom", total_votes=0, plus_votes=0)

	# Try'na get a grip here
    def test_sanity_check(self):
        self.assertTrue(1 == 1)
	
	def 

