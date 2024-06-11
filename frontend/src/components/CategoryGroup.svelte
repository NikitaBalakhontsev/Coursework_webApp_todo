<script lang="ts">
  import Card from "./Card.svelte";
  import RenameModal from "./modals/RenameCategoryModal.svelte";
  import DeleteModal from "./modals/DeleteCategoryModal.svelte";

  import { onMount } from "svelte";
  import type { Task } from "../types";

  export let id: number;
  export let title: string;
  export let cards: Task[];

  export let onCategoryUpdate: () => void;

  const cardWidth = 300; // Ширина карточки
  const gap = 16; // Отступ между карточками и категориями

  let showRenameModal = false;
  let showDeleteModal = false;
  let showAddCardModal = false;
  let showOptions = false;
  let optionsStyle = "";

  onMount(() => {
    document.addEventListener("click", handleClickOutside, true);
  });

  const toggleOptions = (event: MouseEvent) => {
    showOptions = !showOptions;

    if (showOptions) {
      const parentRect = (
        event.currentTarget as HTMLElement
      ).getBoundingClientRect();
      optionsStyle = `top: ${parentRect.top}px; left: ${parentRect.right + 10}px;`;
    }
  };

  const openRenameModal = () => {
    showOptions = false;
    showRenameModal = true;
  };

  const openDeleteModal = () => {
    showOptions = false;
    showDeleteModal = true;
  };

  const closeModals = () => {
    showRenameModal = false;
    showDeleteModal = false;
  };

  const handleCategoryUpdate = () => {
    closeModals();
    onCategoryUpdate();
  };

  function handleClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.closest(`.category-${id}`)) {
      showOptions = false;
    }
  }

  const addCategory = () => {
    showAddCardModal = true;
  };
</script>

<div
  class="category-group category-{id}"
  style="width: {cardWidth + gap * 2}px;"
>
  <div class="category-header">
    <h2>{title}</h2>
    <button class="settings-button" on:click={toggleOptions}>⚙️</button>
    {#if showOptions}
      <div class="options-list" style={optionsStyle}>
        <button on:click={openRenameModal}>Переименовать</button>
        <button on:click={openDeleteModal}>Удалить</button>
      </div>
    {/if}
  </div>
  <div class="cards" style="gap: {gap}px;">
    {#each cards as card (card.id)}
      <Card
        id={card.id}
        title={card.title}
        description={card.description}
        date={card.due_date}
        tags={card.tags}
        width={`${cardWidth}px`}
      />
    {/each}
  </div>
</div>

{#if showRenameModal}
  <RenameModal
    {title}
    {id}
    on:close={closeModals}
    on:rename={handleCategoryUpdate}
  />
{/if}

{#if showDeleteModal}
  <DeleteModal
    {title}
    {id}
    on:close={closeModals}
    on:delete={handleCategoryUpdate}
  />
{/if}

<style>
  .category-group {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
  }

  .category-group h2 {
    margin-left: 1rem;
    color: black;
  }

  .category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .settings-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.5em;
    color: black;
  }

  .options-list {
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 150px;
    text-align: left;
    z-index: 1000;
  }

  .options-list button {
    width: 100%;
    padding: 10px;
    margin: 0;
    border: none;
    background: none;
    cursor: pointer;
    text-align: left;
  }

  .options-list button:hover {
    background: #f0f0f0;
  }
</style>
