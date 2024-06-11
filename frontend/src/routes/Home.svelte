<script lang="ts">
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";
  import Card from "../components/Card.svelte";

  const currentRoute = window.location.pathname;
</script>

<Header {currentRoute} />
<main>
  <h1>Home page</h1>
</main>

<Footer />

<style>
</style>
