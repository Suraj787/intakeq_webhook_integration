import frappe
import requests
import json

id_mappings = {
	'lxsn-1': 'first_name',
	'lxsn-2': 'middle_name'
}

@frappe.whitelist(allow_guest=True)
def add_patient():
	kargs = json.loads(frappe.request.data)	
	intake_id = kargs.get('IntakeId')
	url = 'https://intakeq.com/api/v1/intakes/%s'%(intake_id)

	response = requests.get(url, headers={'X-Auth-Key': '03c9e24af5033bdfed0d1d90380bc9933e05aa4c'})
	try:
		data = response.json()
		client_name = data['ClientName']
		client_email = data['ClientEmail']
		client_id = data['ClientId']
		intake_id = data['Id']
		questionaire_name = data['QuestionnaireName']
		questionaire_id = data['QuestionnaireId']
		gender = data['Gender']

		patient = frappe.get_doc({
			'doctype': 'Patient',
			'sex': 'Male', 
			'patient_name': client_name,
			'intake_client_id': client_id,
			'email': client_email,
			'questionaire_id': questionaire_id,
			'intake_id': intake_id
		})

		for question in data['Questions']:
			question_type = question['QuestionType']
			if question_type == 'OpenQuestion':
				pass
			elif question_type == 'MultipleChoice':
				pass
			elif question_type == 'Attachment':
				pass
			elif question_type == 'Matrix':
				pass

		patient.insert(ignore_permissions=True)
		frappe.db.commit()

		return True
	except:
		return False
