<script lang="ts">
  export let id: number;
  export let title: string;
  export let description: string;
  export let date: string | null = null;
  export let width: string = "300px"; // Дефолтное значение ширины
  export let tags: Array<{
    id: number;
    color: string;
    description: string | null;
  }> = []; // Добавление id в tags
</script>

<div class="card {id}" style="width: {width};">
  {#if tags.length > 0}
    <div class="tags-container">
      {#each tags as tag (tag.id)}
        <span class="tag" style="background-color: {tag.color};">
          {#if tag.description}
            <p>{tag.description}</p>
          {/if}
        </span>
      {/each}
    </div>
  {/if}
  <div class="card-header">
    <h3>{title}</h3>
  </div>
  <div class="card-body">
    <p class="description">{description}</p>
  </div>
  {#if date}
    <div class="date-container">
      <p class="date-p">{date}</p>
    </div>
  {/if}
</div>

<style>
  .card {
    display: grid;
    grid-template-rows: auto auto 1fr;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    margin: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    background-color: #716f6a;
    color: #fff;
  }

  .tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .tag {
    padding: 0px 8px;
    border-radius: 4px;
    border-style: solid;
    border-width: 2px;
    border-color: black;
    color: #fff;
    font-size: 0.8rem;
    font-weight: 700;
    text-align: center;
    min-width: 4rem; /* Минимальная ширина для пустых тегов */
    height: 1.5rem; /* Фиксированная высота для всех тегов */
  }

  .card-header {
    text-align: left;
  }

  .card-header h3 {
    margin: 0;
    font-size: 1.2rem;
  }

  .card-body {
    overflow: hidden;
    text-align: left;
  }

  .description {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 1rem;
  }

  .date-container {
    display: flex;
    justify-content: end;
    margin-top: 0.5rem;
  }

  .date-p {
    width: 120px;
    border-style: solid;
    border-radius: 8px;
    bottom: 0;
    font-size: 1rem;
    color: #dfd3d3;
  }
</style>
