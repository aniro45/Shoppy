from app import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == '__main__':
    print("Starting ShopEase in debug mode...")
    print("API endpoints should be available at http://127.0.0.1:5000/products, etc.")
    print("View all registered routes at http://127.0.0.1:5000/debug/routes")
    app.run(debug=True)
