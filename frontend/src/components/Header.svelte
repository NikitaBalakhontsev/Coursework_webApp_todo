<script lang="ts">
  import { onMount } from "svelte";
  import { Link, links, useLocation } from "svelte-routing";
  import { token } from "../stores/authStore";
  import { clearToken } from "../stores/authStore";

  export let currentRoute: string;

  let navToggle: HTMLElement | null;
  let navWrapper: HTMLElement | null;
  let isAuthenticated: boolean = false;

  // Функция для определения, является ли ссылка текущим маршрутом
  const isActive = (path: string) => path === currentRoute;

  onMount(() => {
    // Выбираем элементы после монтирования компонента
    navToggle = document.querySelector(".nav__toggle");
    navWrapper = document.querySelector(".nav__wrapper");

    if (navToggle && navWrapper) {
      // Добавляем обработчик событий клика
      navToggle.addEventListener("click", function () {
        if (navWrapper && navWrapper.classList.contains("active")) {
          this.setAttribute("aria-expanded", "false");
          this.setAttribute("aria-label", "menu");
          navWrapper.classList.remove("active");
        } else if (navWrapper) {
          navWrapper.classList.add("active");
          this.setAttribute("aria-label", "close menu");
          this.setAttribute("aria-expanded", "true");
        }
      });
    } else {
      console.error("NavToggle or NavWrapper element not found");
    }
  });

  // Подписываемся на изменения токена
  token.subscribe((value) => {
    isAuthenticated = !!value;
  });

  // Функция для обработки выхода из аккаунта
  const handleLogout = () => {
    clearToken(); // Вызываем функцию для очистки токена
  };
</script>

<header class="site-header">
  <div class="wrapper site-header__wrapper">
    <div class="site-header__start" use:links>
      <a href="/" class="brand">To-do app</a>
    </div>
    <div class="site-header__middle">
      <nav class="nav" use:links>
        <button class="nav__toggle" aria-expanded="false" type="button">
          меню
        </button>
        <ul class="nav__wrapper">
          {#if !isActive("/")}
            <li class="nav__item"><a href="/">Home</a></li>
          {/if}
          {#if !isActive("/workspace")}
            <li class="nav__item">
              <a href="/workspace">Workspace</a>
            </li>
          {/if}
          {#if !isActive("/about")}
            <li class="nav__item"><a href="/about">About</a></li>
          {/if}
        </ul>
      </nav>
    </div>
    <div class="site-header__end">
      {#if isAuthenticated}
        <a href="/" on:click={handleLogout}>Log out</a>
      {:else}
        <a href="/login">Sign in</a>
        <a href="/authorize">Sign up</a>
      {/if}
    </div>
  </div>
</header>

<style>
  a {
    color: #e85a4f;
  }

  .brand {
    font-weight: bold;
    font-size: 2rem;
  }

  .site-header {
    position: relative;
    width: 100%;
  }

  .site-header__wrapper {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding-top: 1rem;
    padding-bottom: 1rem;
  }

  .site-header__end a {
    font-size: 1.5rem;
    padding: 1rem;
  }

  @media (min-width: 660px) {
    .site-header__wrapper {
      padding-top: 0;
      padding-bottom: 0;
    }
  }
  @media (max-width: 659px) {
    .site-header__end {
      padding-right: 4rem;
    }
  }

  @media (min-width: 660px) {
    .nav__wrapper {
      display: flex;
    }
  }

  @media (max-width: 659px) {
    .nav__wrapper {
      position: absolute;
      top: 100%;
      right: 0;
      left: 0;
      z-index: -1;
      background-color: #d9f0f7;
      visibility: hidden;
      opacity: 0;
      transform: translateY(-100%);
      transition:
        transform 0.3s ease-out,
        opacity 0.3s ease-out;
    }
  }

  .nav__item a {
    display: block;
    padding: 1.5rem 1rem;
    font-size: 1.5rem;
  }

  .nav__toggle {
    display: none;
  }
  @media (max-width: 659px) {
    .nav__toggle {
      display: block;
      position: absolute;
      right: 1rem;
      top: 1rem;
    }
  }
</style>
