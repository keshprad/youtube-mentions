<script>
  // External Imports
  import "../../theme/theme.scss";
  import Button, { Label } from "@smui/button";
  import Card, { Actions, ActionIcons, Content } from "@smui/card";
  import IconButton from "@smui/icon-button";

  // Props
  export let song;
</script>

<Card style="width: 100%;">
  <Content style="padding-bottom: 0;">
    <div class="content-container">
      <div class="img-container">
        <img src={song["image"]} alt="song" />
      </div>
      <div class="text-container">
        <p class="title">{song["title"]}</p>
        <p>by {song["artists"]}</p>
      </div>
    </div>
  </Content>
  <Actions>
    <ActionIcons>
      <Button
        style="margin: 0;"
        href={song["links"]["shazam"]}
        target="_blank"
        color="primary"
      >
        <Label>Shazam</Label>
      </Button>
      <IconButton href={song["links"]["apple"]} target="_blank" color="primary">
        <i class="fas fa-music" />
      </IconButton>
      <IconButton
        href={song["links"]["spotify"]}
        target="_blank"
        color="primary"
      >
        <i class="fab fa-spotify" />
      </IconButton>
    </ActionIcons>
  </Actions>
</Card>

<style>
  .content-container {
    width: 100%;
    display: flex;
  }
  .img-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 10px;
    width: 40%;
    min-width: 100px;
  }
  .img-container img {
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
  .text-container .title {
    font-weight: bold;
    font-style: italic;
  }
  i {
    color: var(--mdc-theme-primary);
  }
</style>
