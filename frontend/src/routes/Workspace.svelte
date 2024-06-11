<script lang="ts">
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";
  import CategoryGroup from "../components/CategoryGroup.svelte";
  import AddCategoryModal from "../components/modals/AddCategoryModal.svelte";

  import { token } from "../stores/authStore";
  import { navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { fetchCategories } from "../api/category";
  import { fetchTasks } from "../api/task";
  import type { Category, Task } from "../types";

  const currentRoute = window.location.pathname;

  let categories: Category[] = [];

  let isAuthenticated = false;
  let showModal = false;

  const loadCategoriesAndTasks = async () => {
    try {
      const fetchedCategories = await fetchCategories();

      const categoriesWithTasks = await Promise.all(
        fetchedCategories.map(async (category: any) => {
          const tasks = await fetchTasks(category.id);
          return { ...category, title: category.name, cards: tasks };
        })
      );
      categories = categoriesWithTasks;
    } catch (error) {
      console.error("Error fetching categories or tasks:", error);
    }
  };

  const handleCategoryAdded = async (event: CustomEvent) => {
    showModal = false;
    await loadCategoriesAndTasks();
  };

  onMount(() => {
    const unsubscribe = token.subscribe(async (value) => {
      isAuthenticated = !!value;
      if (!isAuthenticated) {
        navigate("/login");
      } else {
        await loadCategoriesAndTasks();
      }
    });

    return () => unsubscribe();
  });

  const addCategory = () => {
    showModal = true;
  };
</script>

<Header {currentRoute} />

{#if isAuthenticated}
  <main>
    <div class="categories-wrapper">
      <div class="categories-container">
        {#each categories as category (category.id)}
          <CategoryGroup
            id={category.id}
            title={category.title}
            cards={category.cards}
            onCategoryUpdate={loadCategoriesAndTasks}
          />
        {/each}
        <button class="add-category-button" on:click={addCategory}
          >Добавить колонку</button
        >
      </div>
    </div>
    {#if showModal}
      <AddCategoryModal
        on:categoryAdded={handleCategoryAdded}
        on:cancel={() => (showModal = false)}
      />
    {/if}
  </main>
{/if}

<Footer />

<style>
  main {
    display: flex;
    flex-direction: column;
    height: calc(100vh - var(--header-height) - var(--footer-height));
    overflow: hidden;
  }

  .categories-wrapper {
    flex: 1;
    overflow-x: auto;
    overflow-y: hidden;
    display: flex;
    align-items: flex-start;
    width: 100%;
  }

  .categories-container {
    display: flex;
    gap: 16px;
    padding: 1rem;
    align-items: flex-start;
  }

  .add-category-button {
    padding: 16px;
    border: 1px dashed #bbb;
    background: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-size: 1rem;
    color: #555;
    min-width: 250px;
    height: fit-content;
  }

  .add-category-button:hover {
    border-color: #888;
    color: #333;
  }
</style>
