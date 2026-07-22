module.exports = async ({ github, context, core }) => {
  const owner = context.repo.owner;
  const repo = context.repo.repo;

  const data = await github.graphql(
    `query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        id
        discussionCategories(first: 25) {
          nodes { id name slug }
        }
        discussions(first: 100) {
          nodes { title }
        }
      }
    }`,
    { owner, repo },
  );

  const repository = data.repository;
  const existing = new Set(repository.discussions.nodes.map((discussion) => discussion.title));
  const categories = new Map(
    repository.discussionCategories.nodes.map((category) => [category.slug, category.id]),
  );

  const seeds = [
    {
      slug: "announcements",
      title: "Welcome to I Have ADHD and 47 Tabs",
      body: `This is the community space for installation help, ideas, translations, and real before-and-after examples.

Start with the latest release, use Q&A for help, and use Show and tell to share a result with private details removed.

This project is a response-formatting tool, not medical advice or diagnosis.`,
    },
    {
      slug: "show-and-tell",
      title: "Share the AI answer that made you install this",
      body: `What answer made you think, “my AI has 47 tabs open too”?

Share a short before-and-after example with names, private conversations, and sensitive information removed. Include the platform you used and the part of the skill that helped most.`,
    },
    {
      slug: "general",
      title: "Which platform are you using it with?",
      body: `Comment with the platform where you use the skill most and anything that made installation easier or harder.

Suggested choices: Claude, ChatGPT, Custom GPT, Codex, GitHub Copilot, and another Agent Skills host.`,
    },
    {
      slug: "ideas",
      title: "Which language should we translate next?",
      body: `Reply with the language and region you would use, whether you can review a translation, and which platform you would test it on.

Translations should preserve the behavioral meaning, avoid medical claims, and retain upstream attribution.`,
    },
  ];

  for (const seed of seeds) {
    if (existing.has(seed.title)) {
      core.info(`Already exists: ${seed.title}`);
      continue;
    }

    const categoryId = categories.get(seed.slug);
    if (!categoryId) {
      core.warning(`Missing discussion category '${seed.slug}', skipping '${seed.title}'.`);
      continue;
    }

    const result = await github.graphql(
      `mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
        createDiscussion(input: {
          repositoryId: $repositoryId,
          categoryId: $categoryId,
          title: $title,
          body: $body
        }) {
          discussion { url }
        }
      }`,
      {
        repositoryId: repository.id,
        categoryId,
        title: seed.title,
        body: seed.body,
      },
    );

    core.info(`Created: ${seed.title} (${result.createDiscussion.discussion.url})`);
    existing.add(seed.title);
  }
};
