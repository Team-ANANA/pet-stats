CREATE TABLE `animals` (
  `id` int PRIMARY KEY NOT NULL,
  `organization_id` varchar(255) NOT NULL,
  `type_id` int,
  `species` varchar(255),
  `primary_breed_id` int,
  `secondary_breed_id` int,
  `mixed_breed` boolean,
  `unknown_breed` boolean,
  `primary_color_id` int,
  `secondary_color_id` int,
  `tertiary_color_id` int,
  `age` varchar(255),
  `gender_id` int,
  `size` varchar(255),
  `coat_id` int,
  `spayed_neutered` boolean,
  `house_trained` boolean,
  `declawed` boolean,
  `special_needs` boolean,
  `shots_current` boolean,
  `environment_children` boolean,
  `environment_dogs` boolean,
  `environment_cats` boolean,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `published_at` timestamp NOT NULL
);

CREATE TABLE `tags` (
  `id` int,
  `descriptor` varchar(255)
);

CREATE TABLE `type` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL
);

CREATE TABLE `coat` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `descriptor` varchar(255) NOT NULL
);

CREATE TABLE `color` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `descriptor` varchar(255) NOT NULL
);

CREATE TABLE `genders` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `descriptor` varchar(255) NOT NULL
);

CREATE TABLE `breed` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `descriptor` varchar(255) NOT NULL
);

CREATE TABLE `organization` (
  `id` varchar(255) PRIMARY KEY NOT NULL,
  `name` varchar(255) NOT NULL,
  `address1` varchar(255),
  `address2` varchar(255),
  `city` varchar(255),
  `postcode` varchar(255),
  `country` varchar(255)
);

ALTER TABLE `animals` ADD FOREIGN KEY (`organization_id`) REFERENCES `organization` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`type_id`) REFERENCES `type` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`primary_breed_id`) REFERENCES `breed` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`secondary_breed_id`) REFERENCES `breed` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`primary_color_id`) REFERENCES `color` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`secondary_color_id`) REFERENCES `color` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`tertiary_color_id`) REFERENCES `color` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`gender_id`) REFERENCES `genders` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`coat_id`) REFERENCES `coat` (`id`);

ALTER TABLE `tags` ADD FOREIGN KEY (`id`) REFERENCES `animals` (`id`);

ALTER TABLE `coat` ADD FOREIGN KEY (`type_id`) REFERENCES `type` (`id`);

ALTER TABLE `color` ADD FOREIGN KEY (`type_id`) REFERENCES `type` (`id`);

ALTER TABLE `genders` ADD FOREIGN KEY (`type_id`) REFERENCES `type` (`id`);

ALTER TABLE `breed` ADD FOREIGN KEY (`type_id`) REFERENCES `type` (`id`);
