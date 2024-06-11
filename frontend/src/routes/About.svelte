<script>
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";
  const currentRoute = window.location.pathname;
</script>

<Header {currentRoute} />
<main>
  <h1>About</h1>
  <form></form>
</main>

<Footer />

<style>
</style>
