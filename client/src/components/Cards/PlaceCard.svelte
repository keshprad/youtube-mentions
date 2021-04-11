<script>
  // External Imports
  import "../../theme/theme.scss";
  import Button, { Label } from "@smui/button";
  import Card, { Actions, ActionIcons, Content } from "@smui/card";
  import IconButton from "@smui/icon-button";

  // Props
  export let place;
</script>

<Card style="width: 100%;">
  <Content style="padding-bottom: 0;">
    <div class="content-container">
      <div class="left-container">
        {#if place["image"]}
           <img src={place["image"]} alt={place['name']} />
        {/if}
        <p><strong>timestamp:</strong> {(place['time']['start']/60).toFixed(0)}:{(place['time']['start']%60).toFixed(0).padStart(2, '0')}</p>
      </div>
      <div class="text-container">
        <p class="name">{place["name"]}</p>
        <p class="summary">{place["summary"]}</p>
      </div>
    </div>
  </Content>
  <Actions>
    <ActionIcons>
      {#if place["links"].hasOwnProperty("wikipedia")}
        <IconButton
          href={place["links"]["wikipedia"]}
          target="_blank"
          color="primary"
        >
          <i class="fab fa-wikipedia-w" />
        </IconButton>
      {/if}
    </ActionIcons>
  </Actions>
</Card>

<style>
  .content-container {
    width: 100%;
    display: flex;
  }
  .left-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-right: 10px;
    width: 40%;
    min-width: 100px;
  }
  .left-container img {
    width: 100%;
    height: auto;
  }
  .text-container {
    margin-left: 10px;
    text-align: center;
    font-size: 1.2rem;
    width: 60%;
  }
  .text-container > p {
    margin: 10px;
  }
  .text-container .name {
    font-weight: bold;
  }
  .text-container .summary {
    font-size: 1rem;
    text-align: start;
  }
  .genre {
    font-style: italic;
    font-size: 1rem;
  }
  i {
    color: var(--mdc-theme-primary);
  }
</style>
