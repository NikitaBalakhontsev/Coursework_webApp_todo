<script>
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";

  import Login from "../components/Login.svelte";

  const currentRoute = window.location.pathname;
</script>

<Header {currentRoute} />

<main>
  <h1>Login</h1>
  <Login />
</main>

<Footer />

<style>
  h1 {
    padding-bottom: 20px;
    color: #e85a4f;
  }
</style>
