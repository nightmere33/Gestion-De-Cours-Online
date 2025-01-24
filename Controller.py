from Model import CourseModel

class CourseController:
    def __init__(self):
        self.model = CourseModel()

    def ajouter_cours(self, data):
        # Validate and add course
        if all(data):
            self.model.ajouter_cours(data)
            return True
        return False

    def modifier_cours(self, course_id, new_data):
        # Update course
        self.model.modifier_cours(course_id, new_data)

    def supprimer_cours(self, course_id):
        # Delete course
        self.model.supprimer_cours(course_id)

    def consulter_cours(self):
        # Get all courses
        return self.model.consulter_cours()

    def rechercher_cours(self, titre):
        # Search courses
        return self.model.rechercher_cours(titre)