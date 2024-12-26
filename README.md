# Neothink

Neothink is an AI-powered project management software designed for enterprise use. It leverages advanced machine learning algorithms to streamline project workflows, enhance team collaboration, and provide actionable insights for better decision-making.

## Getting Started

### Frontend

1. Clone the repository:
   ```bash
   git clone https://github.com/neothink-ai/neothink.git
   ```

2. Navigate to the project directory:
   ```bash
   cd neothink
   ```

3. Install the frontend dependencies:
   ```bash
   npm install
   ```

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

## Running the Application

1. Ensure the backend server is running:
   ```bash
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173` to view the application.

## Building for Production

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with:

```bash
npm run preview
```

