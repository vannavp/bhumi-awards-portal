# Copyright (c) 2021, Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Vote(Document):
	def validate(self):
		# The voter should not have voted before
		# Get all previous voters
		all_voters = set(frappe.get_all('Vote', pluck='voter'))
		if self.voter in all_voters:
			frappe.throw('You have already voted!')

	def before_save(self):
		voter = frappe.get_doc('User', self.voter)
		self.voter_name = voter.full_name
		
	def after_insert(self):
		# Increase the vote count for this particular college
		self.increment_vote_count()

	def increment_vote_count(self):
		college = frappe.get_doc('College', self.college)
		college.total_votes = college.total_votes + 1
		college.save()