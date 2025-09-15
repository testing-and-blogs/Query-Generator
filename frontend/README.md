# Frontend Application

This directory contains the source code for the frontend of the Schema-Aware NLQ platform.

## Framework Choice (TBD)

As per the project specification, the choice of React framework is to be decided between **Next.js** and **Vite + React**. This scaffolding has been set up to support either choice.

The `package.json` file in this directory includes all the necessary dependencies for the application, such as `react`, `tailwindcss`, `reactflow`, `zustand`, etc., as well as the development dependencies for both Next.js and Vite.

## Getting Started: Next Steps

To initialize the project, please follow the instructions for your chosen framework. You will essentially be initializing the framework *into this existing directory*.

### Option 1: Using Next.js

1.  **Initialize Next.js:**
    Run the `create-next-app` command in the *parent* directory (`repo/`), telling it to use the existing `frontend` directory.

    ```bash
    # Run from the repository root
    npx create-next-app@latest frontend --typescript --tailwind --eslint
    ```

2.  **Merge `package.json`:**
    The initializer may create a new `package.json`. Manually merge the dependencies from the original `package.json` (the one in this scaffolding) into the newly created one. Then, delete the temporary `package.json` created by the tool if necessary.

3.  **Install Dependencies:**
    ```bash
    cd frontend
    npm install
    ```

### Option 2: Using Vite

1.  **Initialize Vite:**
    Run the `create-vite` command. You can do this inside the `frontend` directory.

    ```bash
    # Run from the repository root
    cd frontend
    npm create vite@latest . -- --template react-ts
    ```
    The `.` tells Vite to use the current directory.

2.  **Merge `package.json`:**
    Vite will prompt you before overwriting `package.json`. You can let it, and then manually merge the dependencies from the scaffolding `package.json` into the new one.

3.  **Install Dependencies:**
    ```bash
    npm install
    ```

4.  **Set up Tailwind CSS:**
    You will need to follow the official Vite guide to integrate Tailwind CSS, which involves creating `tailwind.config.js` and `postcss.config.js`.

After completing these steps, you can run the development server (e.g., `npm run dev`) and begin building the components as outlined in the project specification.
