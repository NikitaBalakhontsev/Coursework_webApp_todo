<script lang="ts">
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";
  import CategoryGroup from "../components/CategoryGroup.svelte";
  import { token } from "../stores/authStore";
  import { navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { fetchCategories } from "../api/category";
  import { fetchTasks } from "../api/task";
  import type { Category, Task } from "../types";

  const currentRoute = window.location.pathname;
  let isAuthenticated = false;
  let categories: Category[] = [];

  const loadCategoriesAndTasks = async () => {
    try {
      console.log("начало загрузки категорий");
      const fetchedCategories = await fetchCategories();
      console.log(fetchCategories);

      console.log("Начало загрузки карточек");
      const categoriesWithTasks = await Promise.all(
        fetchedCategories.map(async (category: Category) => {
          const tasks = await fetchTasks(category.id);
          return { ...category, cards: tasks };
        })
      );
      categories = categoriesWithTasks;
      console.log(categoriesWithTasks);
    } catch (error) {
      console.error("Error fetching categories or tasks:", error);
    }
  };

  onMount(() => {
    const unsubscribe = token.subscribe(async (value) => {
      isAuthenticated = !!value;
      if (!isAuthenticated) {
        navigate("/login");
      } else {
        console.log("начали грузить карточки");

        await loadCategoriesAndTasks();
      }
    });

    return () => unsubscribe();
  });
</script>

<Header {currentRoute} />

{#if isAuthenticated}
  <main>
    {#each categories as category (category.id)}
      <CategoryGroup title={category.title} cards={category.cards} />
    {/each}
  </main>
{/if}

<Footer />

<style>
  main {
    display: grid;
    grid-template-columns: repeat(auto-fill, 300px);
    gap: 16px;
    padding: 0 1rem 0 1rem;
    background-color: #eae7dc;
  }
</style>
