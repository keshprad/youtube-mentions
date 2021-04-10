<script>
  // External Imports
  import "../../theme/theme.scss";
  import Button, { Label } from "@smui/button";
  import Card, { Actions, Content } from "@smui/card";

  // Props
  export let card;
</script>

<Card style="width: 100%">
  <Content>{card.content}</Content>
  <Actions fullBleed>
    <Button href={card.wiki_link} target="_blank">
      <Label>Wikipedia</Label>
      <i class="material-icons" aria-hidden="true">arrow_forward</i>
    </Button>
  </Actions>
</Card>

<style>
</style>
