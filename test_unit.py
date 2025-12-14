import unittest
from app import app
from models import db, Employee, User, PickupRequest

class BasicTests(unittest.TestCase):

    def setUp(self):
        # Set up a temporary database for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Seed a user for requests
            u = User(username='TestUser', email='test@example.com', password='pw')
            db.session.add(u)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_employee(self):
        # Test C in CRUD
        response = self.app.post('/api/employees', json={
            'name': 'Unit Test Emp',
            'email': 'unit@test.com',
            'role': 'Employee'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Unit Test Emp', str(response.data))

    def test_read_employees(self):
        # Test R in CRUD
        self.app.post('/api/employees', json={'name': 'E1', 'email': 'e1@t.com', 'role': 'E'})
        response = self.app.get('/api/employees')
        self.assertEqual(response.status_code, 200)
        self.assertIn('E1', str(response.data))

    def test_delete_employee(self):
        # Test D in CRUD
        # 1. Create
        res = self.app.post('/api/employees', json={'name': 'To Delete', 'email': 'del@t.com', 'role': 'E'})
        emp_id = res.json['id']
        
        # 2. Delete
        del_res = self.app.delete(f'/api/employees/{emp_id}')
        self.assertEqual(del_res.status_code, 200)
        
        # 3. Verify Gone
        get_res = self.app.get('/api/employees')
        self.assertNotIn('To Delete', str(get_res.data))

if __name__ == "__main__":
    unittest.main()

