<script lang="ts">
  let todos = [
    { id: 1, text: "Hack the mainframe", done: false },
    { id: 2, text: "Buy synthetic milk", done: true },
    { id: 3, text: "Update cyberdeck drivers", done: false }
  ];

  const asciiFace = "(◕‿◕)";
</script>

<div class="app-shell">
  <!-- Main Face Container -->
  <header class="face-container">
    <pre class="ascii-face">{asciiFace}</pre>
    <div class="status-indicator">ONLINE</div>
  </header>

  <!-- TODO List -->
  <main class="todo-list">
    {#each todos as todo}
      <div class="todo-item" class:done={todo.done}>
        <div class="todo-content">
          <span class="bullet">></span>
          <span class="text">{todo.text}</span>
        </div>
        <div class="deco-line"></div>
      </div>
    {/each}
  </main>
</div>

<style>
  :root {
    --ink-black: #1a1a1a;
    --paper-white: #ffffff;
    --accent-gray: #e0e0e0;
    --soft-shadow: rgba(0, 0, 0, 0.1);
    font-family: 'JetBrains Mono', 'Courier New', monospace;
  }

  :global(body) {
    margin: 0;
    padding: 10px;
    background: var(--paper-white);
    overflow: hidden;
    color: var(--ink-black);
    user-select: none;
  }

  .app-shell {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 280px;
  }

  .face-container {
    background: var(--paper-white);
    border: 2px solid var(--ink-black);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: fit-content;
    border-radius: 4px;
    position: relative;
    box-shadow: 4px 4px 0px var(--soft-shadow);
    clip-path: polygon(0 0, 100% 0, 100% 80%, 90% 100%, 0 100%);
  }

  .ascii-face {
    margin: 0;
    font-size: 1.3rem;
    font-weight: 800;
  }

  .status-indicator {
    font-size: 0.65rem;
    letter-spacing: 2px;
    padding-left: 15px;
    font-weight: 700;
    color: #444;
  }

  .todo-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .todo-item {
    background: var(--paper-white);
    border: 2px solid var(--ink-black);
    padding: 8px 12px;
    font-size: 0.9rem;
    position: relative;
    transition: all 0.15s ease-out;
    width: calc(100% - 24px);
    border-radius: 2px;
    box-shadow: 3px 3px 0px var(--soft-shadow);
  }

  .todo-item:hover {
    transform: translate(-2px, -2px);
    box-shadow: 5px 5px 0px var(--ink-black);
  }

  .todo-content {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .bullet {
    font-weight: 900;
    color: #000;
  }

  .done .text {
    text-decoration: line-through;
    opacity: 0.3;
  }

  .text {
    font-weight: 500;
  }

  .deco-line {
    height: 2px;
    background: var(--ink-black);
    width: 30px;
    margin-top: 6px;
    opacity: 0.8;
  }

  /* Scrollbar override */
  ::-webkit-scrollbar {
    width: 0px;
  }
</style>


