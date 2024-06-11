<script>
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";

  import Authorize from "../components/Authorize.svelte";

  const currentRoute = window.location.pathname;
</script>

<Header {currentRoute} />

<main>
  <h1>Registration</h1>
  <Authorize />
</main>
<Footer />

<style>
  h1 {
    padding-bottom: 20px;
    color: #e85a4f;
  }
</style>
