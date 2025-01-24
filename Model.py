import mysql.connector

class CourseModel:
    def __init__(self):
        # Establish database connection
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='platform_courses'
        )
        self.cursor = self.conn.cursor()
        self.creer_table()

    def creer_table(self):
        # Create the courses table if it doesn't exist
        query = """
        CREATE TABLE IF NOT EXISTS cours (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titre VARCHAR(100),
            description TEXT,
            categorie VARCHAR(25),
            niveau VARCHAR(20),
            duree INT,
            instructeur VARCHAR(25),
            date_publication DATE
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def ajouter_cours(self, data):
        # Add a new course to the database
        query = """
        INSERT INTO cours 
        (titre, description, categorie, niveau, duree, instructeur, date_publication) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, data)
        self.conn.commit()

    def modifier_cours(self, course_id, new_data):
        # Update an existing course
        query = """
        UPDATE cours 
        SET titre=%s, description=%s, categorie=%s, niveau=%s, 
            duree=%s, instructeur=%s, date_publication=%s 
        WHERE id=%s
        """
        self.cursor.execute(query, new_data + (course_id,))
        self.conn.commit()

    def supprimer_cours(self, course_id):
        # Delete a course
        query = "DELETE FROM cours WHERE id=%s"
        self.cursor.execute(query, (course_id,))
        self.conn.commit()

    def consulter_cours(self):
        # Get all courses
        query = "SELECT * FROM cours"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def rechercher_cours(self, titre):
        # Search courses by title
        query = "SELECT * FROM cours WHERE titre LIKE %s"
        self.cursor.execute(query, (f"%{titre}%",))
        return self.cursor.fetchall()