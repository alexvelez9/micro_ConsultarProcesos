from micro_consultaprocesos import create_app


class main():
    """Objeto principal del programa."""

    def run(self) -> None:
        """Secuencia logica del programa.

        Keyword arguments:
        None.
        Return: None
        """
        try:
            app = create_app()
            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=9002)
        except TypeError as terr:
            print(f'Error en main.run(): {terr}')


runprog = main()
runprog.run()
