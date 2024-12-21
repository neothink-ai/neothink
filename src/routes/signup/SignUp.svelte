
<script>
    import { authHandlers, error} from '../../lib/stores/authStore';
    let email = '';
    let password = '';
    let confirmPassword = '';
    
    async function handleSignup() {
        if (password !== confirmPassword) {
            $error = "Passwords don't match";
            return;
        }
        
        try {
            await authHandlers.signup(email, password);
            // Redirect to home page or dashboard
            window.location.href = '/';
        } catch (err) {
            // Error is already handled in the store
            console.error('Signup failed:', err);
        }
    }
</script>

<div class="signup-container">
    <h1>Sign Up</h1>
    
    {#if $error}
        <div class="error-message">
            {$error}
        </div>
    {/if}
    
    <form on:submit|preventDefault={handleSignup}>
        <div class="form-group">
            <label for="email">Email</label>
            <input
                type="email"
                id="email"
                bind:value={email}
                required
            />
        </div>
        
        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                bind:value={password}
                required
                minlength="6"
            />
        </div>
        
        <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
                type="password"
                id="confirmPassword"
                bind:value={confirmPassword}
                required
                minlength="6"
            />
        </div>
        
        <button type="submit">Sign Up</button>
    </form>
    
    <p>Already have an account? <a href="/login">Login</a></p>
</div>

<style>
    .signup-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .form-group {
        margin-bottom: 1rem;
    }
    
    label {
        display: block;
        margin-bottom: 0.5rem;
    }
    
    input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    
    button {
        width: 100%;
        padding: 0.75rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    
    button:hover {
        background-color: #45a049;
    }
    
    .error-message {
        color: red;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #ffebee;
        border-radius: 4px;
    }
</style>
