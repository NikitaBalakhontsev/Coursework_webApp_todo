<script lang="ts">
  import { navigate } from "svelte-routing";
  import { login } from "../api/auth";

  let email = "";
  let password = "";
  let errorMessage = "";

  async function handleLogin() {
    try {
      await login(email, password);
      navigate("/workspace");
    } catch (error: any) {
      errorMessage =
        error.response?.data?.message || "Unknown error occurred during login";
    }
  }
</script>

<form on:submit|preventDefault={handleLogin}>
  <input type="email" bind:value={email} placeholder="Email" required />
  <input
    type="password"
    bind:value={password}
    placeholder="Password"
    required
  />
  <button type="submit">Login</button>
  {#if errorMessage}
    <p>{errorMessage}</p>
  {/if}
</form>

<style>
  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 400px;
    margin: 0 auto;
  }
  input,
  button {
    padding: 0.5rem;
    font-size: 1rem;
  }

  button {
    color: white;
  }

  p {
    color: red;
  }
</style>
