<script>
  // External Imports
  import { onMount, createEventDispatcher } from "svelte";
  import YoutubePlayer from "youtube-player";

  // My Imports
  import "../theme/colors.js";

  // Props
  export let videoId, updateTime;

  let player;
  let ytEle;
  let options = {
    videoId: videoId,
    playerVars: {
      modestbranding: 1,
    },
  };

  async function startInterval() {
    setInterval(async function () {
      const state = await player.getPlayerState();
      if (state === 1) {
        updateTime(await player.getCurrentTime());
      }
    }, 1000);
  }

  onMount(() => createPlayer());
  $: play(videoId);
  function createPlayer() {
    player = YoutubePlayer(ytEle, options);
    player.on("ready", onPlayerReady);
  }

  const eventDispatcher = createEventDispatcher();
  async function onPlayerReady(event) {
    // play(videoId);
    startInterval();
  }

  function play(videoId) {
    if (player && videoId) {
      player.cueVideoById({ videoId: videoId });
    }
  }
</script>

<div class="vid-container">
  <div bind:this={ytEle} id="player" />
</div>

<style>
  .vid-container {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 56.25%;
  }
  #player {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
</style>
