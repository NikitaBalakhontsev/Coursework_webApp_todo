<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { deleteCategory } from "../../api/category";

  export let title: string;
  export let id: number;

  const dispatch = createEventDispatcher();

  const deleteCategoryAction = async () => {
    try {
      await deleteCategory(id);
      dispatch("delete");
    } catch (error) {
      console.error("Не удалось удалить категорию", error);
    }
  };
</script>

<div class="modal-overlay">
  <div class="modal">
    <h2>Удалить категорию</h2>
    <div class="modal-text">
      <p>Вы собираетесь удалить категорию</p>
      <p><strong>{title}</strong></p>
      <p>Все вложенные карточки будут удалены.</p>
    </div>
    <div class="buttons">
      <button on:click={() => dispatch("close")}>Отмена</button>
      <button on:click={deleteCategoryAction}>Удалить</button>
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

  .modal-text {
    margin-bottom: 1.5rem;
  }

  p {
    font-size: 1.2rem;
    color: black;
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
