<script>
  // External Imports
  import { slide } from "svelte/transition";

  // My Imports
  import PersonCard from "./Cards/PersonCard.svelte";
  import SongCard from "./Cards/SongCard.svelte";
  import ArtistCard from "./Cards/ArtistCard.svelte";

  // Props
  export let currTime, cards;

  $: currentCards = cards.filter((card) => currTime >= card["time"]["start"]);
</script>

<div class="cards-container">
  {#each currentCards as card}
    <div class="card">
      {#if card["card_type"] === "person"}
        <PersonCard {card} />
      {:else if card["card_type"] === "song"}
        <SongCard song={card} />
      {:else if card["card_type"] === "artist"}
        <ArtistCard artist={card} />
      {/if}
    </div>
  {/each}
</div>

<style>
  .cards-container {
    display: flex;
    flex-direction: column-reverse;
    align-items: center;
    overflow-y: scroll;
  }
  .cards-container::-webkit-scrollbar {
    display: none;
  }
  .card {
    color: #262626;
    width: calc(100% - 50px);
    margin: 20px 0;
  }
</style>
