<script>
  // External Imports
  import { slide } from "svelte/transition";

  // My Imports
  import ArtistCard from "./Cards/ArtistCard.svelte";
  import GameCard from "./Cards/GameCard.svelte";
  import PersonCard from "./Cards/PersonCard.svelte";
  import PlaceCard from "./Cards/PlaceCard.svelte";
  import SongCard from "./Cards/SongCard.svelte";

  // Props
  export let currTime, cards;

  $: currentCards = cards.filter((card) => currTime >= card["time"]["start"]);
</script>

<div class="cards-container">
  {#each currentCards as card}
    <div class="card">
      {#if card["card_type"] === "artist"}
        <ArtistCard artist={card} />
      {:else if card["card_type"] === "game"}
        <GameCard game={card} />
      {:else if card["card_type"] === "person"}
        <PersonCard person={card} />
      {:else if card["card_type"] === "place"}
        <PlaceCard place={card} />
      {:else if card["card_type"] === "song"}
        <SongCard song={card} />
      {/if}
    </div>
  {/each}
  {#if currentCards.length === 0 && cards.length > 0}
    <h3>Info will show up here as the video progresses.</h3>
  {/if}
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
