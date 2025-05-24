from emulator import create_app

app = create_app()

if __name__ == '__main__':
    if hasattr(app.panel, "mainloop"):
        # we're running the emulator
        import threading

        def app_runner():
            app.run()

        threading.Thread(target=app_runner, daemon=True).start()
        app.panel.mainloop()
    else:
        # we're running on hardware
        app.run()