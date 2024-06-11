<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { updateCategoryName } from "../../api/category";

  export let title: string;
  export let id: number;

  let newName = title;
  let errorMessage = "";
  const dispatch = createEventDispatcher();

  const renameCategory = async () => {
    if (!newName.trim()) {
      errorMessage = "Название не может быть пустым";
      return;
    }

    try {
      await updateCategoryName(id, newName);
      dispatch("rename");
    } catch (error) {
      errorMessage = "Не удалось переименовать категорию";
    }
  };
</script>

<div class="modal-overlay">
  <div class="modal">
    <h2>Переименовать категорию</h2>
    <input type="text" bind:value={newName} placeholder="Название категории" />
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    <div class="buttons">
      <button on:click={() => dispatch("close")}>Отмена</button>
      <button on:click={renameCategory}>Сохранить</button>
    </div>
  </div>
</div>

<style>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    max-width: 100%;
    text-align: center;
    border-radius: 1rem;
  }

  h2 {
    color: black;
    margin-top: 0;
    margin-bottom: 2rem;
    font-size: 1.8rem;
  }

  input {
    width: 100%;
    margin-bottom: 1.5rem;
    padding: 1rem;
    font-size: 1.2rem;
    border: 1px solid #ccc;
  }

  .error {
    color: red;
    margin: 0 0 1.2rem 0;
    font-size: 1rem;
  }

  .buttons {
    width: 340px;
    display: flex;
    justify-content: space-between;
    font-size: 1.2rem;
  }

  button {
    width: 140px;
    height: 60px;
    text-align: center;
    border: none;
    cursor: pointer;
  }

  button:first-child {
    background: #ccc;
  }

  button:last-child {
    background: #007bff;
    color: white;
  }
</style>
