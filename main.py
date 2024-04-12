import argparse
from user_handler import UserHandler
from course_handler import CourseHandler

def main():
    parser = argparse.ArgumentParser(description="Script para manejar usuarios y cursos")
    parser.add_argument('-create_users', action='store_true', help="Crear usuarios")
    parser.add_argument('-p', '--profile', type=str, help="Perfil de usuario")
    parser.add_argument('-cp', '--password', type=str, help="Contraseña de usuario")
    parser.add_argument('-n', type=int, help="Número de usuarios a crear")

    args = parser.parse_args()

    if args.create_users:
        user_handler = UserHandler()
        user_handler.create_users(args.profile, args.password, args.n)

if __name__ == "__main__":
    main()