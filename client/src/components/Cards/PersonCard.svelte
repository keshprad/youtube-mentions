<script>
  // External Imports
  import "../../theme/theme.scss";
  import Button, { Label } from "@smui/button";
  import Card, { Actions, ActionIcons, Content } from "@smui/card";
  import IconButton from "@smui/icon-button";

  // Props
  export let person;
</script>

<Card style="width: 100%;">
  <Content style="padding-bottom: 0;">
    <div class="content-container">
      <div class="left-container">
        {#if person["image"]}
           <img src={person["image"]} alt={person['name']} />
        {/if}
        <p><strong>timestamp:</strong> {(person['time']['start']/60).toFixed(0)}:{(person['time']['start']%60).toFixed(0).padStart(2, '0')}</p>
      </div>
      <div class="text-container">
        <p class="name">{person["name"]}</p>
        <p class="summary">{person["summary"]}</p>
      </div>
    </div>
  </Content>
  <Actions>
    <ActionIcons>
      {#if person["links"].hasOwnProperty("wikipedia")}
        <IconButton
          href={person["links"]["wikipedia"]}
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
  i {
    color: var(--mdc-theme-primary);
  }
</style>
