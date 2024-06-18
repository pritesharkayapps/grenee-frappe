from frappe.model.document import Document
import frappe

@frappe.whitelist()
def user_get_list():
    user = frappe.session.user
    role_profile_name = frappe.db.get_value('User', user, 'role_profile_name')
    
    if role_profile_name == 'Grenee Admin':
        return frappe.get_list("User", filters={'role_profile_name':'Franchise User'})

# from frappe.desk.reportview import get_list
# get_list['User'] = user_get_list