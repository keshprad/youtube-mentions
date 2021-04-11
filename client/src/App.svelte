<script>
  // External Imports
  import axios from "axios";
  import Button, { Label } from "@smui/button";
  import Icon from "@smui/textfield/icon/index";
  import LinearProgress from "@smui/linear-progress";
  import Textfield from "@smui/textfield";

  // My Imports
  import "./theme/theme.scss";
  import Youtube from "./components/Youtube.svelte";
  import Cards from "./components/Cards.svelte";

  // Props
  export let domain;

  let vidURL = "https://youtu.be/dQw4w9WgXcQ";
  $: vidId = vidURL.split(/[/=]+/).pop();
  let currTime = 0;
  const updateTime = (time) => {
    currTime = Math.floor(time);
  };

  let cardsPromise = () => {
    return axios.get(`${domain}/cards/${vidId}`).then((res) => res.data);
  };
  let loading = false;
</script>

<!-- Adds fonts to head -->
<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
    integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w=="
    crossorigin="anonymous"
  />
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/icon?family=Material+Icons"
  />
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,600,700"
  />
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css?family=Roboto+Mono"
  />
</svelte:head>

<!-- YouTube Mentions -->
<main>
  {#if !loading}
    <div class="left-div">
      <h1 class="welcome">
        Welcome to <span class="title">YouTube Mentions</span>.
      </h1>
      <Label>Enter a YouTube URL</Label>
      <span class="url-input">
        <div class="text-input">
          <Textfield
            variant="outlined"
            dense
            withTrailingIcon
            bind:value={vidURL}
            style="width: 100%;"
          >
            <Icon class="material-icons">play_arrow</Icon>
          </Textfield>
        </div>
        <Button
          class="submit"
          on:click={() => (loading = true)}
          variant="raised"><Label>Submit</Label></Button
        >
      </span>
    </div>
  {:else}
    {#await cardsPromise()}
      <div class="left-div">
        <h2 class="title">YouTube Interact</h2>
        <p>Loading YouTube id: {vidId}</p>
        <div class="progress-bar">
          <LinearProgress indeterminate />
        </div>
      </div>
    {:then cards}
      <div class="left-div">
        <h2 class="title">YouTube Interact</h2>
        <p>Watching {vidId}</p>
        <Youtube videoId={vidId} {updateTime} />
      </div>
      <div class="right-div">
        <Cards {cards} {currTime} />
      </div>
    {/await}
  {/if}
</main>

<style>
  main {
    background-color: #bebebe;
    display: flex;
    flex-direction: row;
    justify-content: center;
    text-align: center;
  }
  main > div {
    height: 100vh;
    padding: 0px 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .left-div {
    flex: 0.7;
    background-color: #bebebe;
    color: #262626;
  }
  .right-div {
    flex: 0.3;
    background-color: #262626;
  }
  h1.welcome {
    margin: 50px 0;
  }
  .title {
    color: var(--mdc-theme-primary);
  }
  div.progress-bar {
    width: 50%;
  }
  span.url-input {
    margin: 20px 0;
    display: flex;
    align-items: center;
  }
  .text-input {
    width: 300px;
    margin-right: 10px;
  }
</style>
