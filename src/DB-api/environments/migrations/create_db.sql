
CREATE TABLE `animals` (
  `id` int PRIMARY KEY NOT NULL,
  `organization_id` varchar(255) NOT NULL,
  `type_id` int,
  `species` varchar(255),
  `primary_breed_id` int,
  `secondary_breed_id` int,
  `is_mixed_breed` boolean,
  `is_unknown_breed` boolean,
  `primary_color_id` int,
  `secondary_color_id` int,
  `tertiary_color_id` int,
  `age` varchar(255),
  `gender_id` int,
  `size` varchar(255),
  `coat_id` int,
  `is_spayed_neutered` boolean,
  `is_house_trained` boolean,
  `is_declawed` boolean,
  `is_special_needs` boolean,
  `is_shots_current` boolean,
  `is_environment_children` boolean,
  `is_environment_dogs` boolean,
  `is_environment_cats` boolean,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `published_at` timestamp NOT NULL
);

CREATE TABLE `animal_tags` (
  `animal_id` int,
  `tag_descriptor` varchar(255)
);

CREATE TABLE `animal_types` (
  `id` int PRIMARY KEY NOT NULL,
  `type_id` int NOT NULL
);

CREATE TABLE `animal_coats` (
  `id` int PRIMARY KEY NOT NULL,
  `type_id` int NOT NULL,
  `coat_descriptor` varchar(255) NOT NULL
);

CREATE TABLE `animal_colors` (
  `id` int PRIMARY KEY NOT NULL,
  `type_id` int NOT NULL,
  `color_descriptor` varchar(255) NOT NULL
);

CREATE TABLE `animal_genders` (
  `id` int PRIMARY KEY NOT NULL,
  `type_id` int NOT NULL,
  `gender_descriptor` varchar(255) NOT NULL
);

CREATE TABLE `animal_breeds` (
  `id` int PRIMARY KEY NOT NULL,
  `type_id` int NOT NULL,
  `breed_descriptor` varchar(255) NOT NULL
);

CREATE TABLE `organizations` (
  `id` varchar(255) PRIMARY KEY NOT NULL,
  `name` varchar(255) NOT NULL,
  `address1` varchar(255),
  `address2` varchar(255),
  `city` varchar(255),
  `postcode` varchar(255),
  `country` varchar(255)
);

ALTER TABLE `animals` ADD FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`type_id`) REFERENCES `animal_types` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`primary_breed_id`) REFERENCES `animal_breeds` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`secondary_breed_id`) REFERENCES `animal_breeds` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`primary_color_id`) REFERENCES `animal_colors` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`secondary_color_id`) REFERENCES `animal_colors` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`tertiary_color_id`) REFERENCES `animal_colors` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`gender_id`) REFERENCES `animal_genders` (`id`);

ALTER TABLE `animals` ADD FOREIGN KEY (`coat_id`) REFERENCES `animal_coats` (`id`);

ALTER TABLE `animal_tags` ADD FOREIGN KEY (`animal_id`) REFERENCES `animals` (`id`);

ALTER TABLE `animal_coats` ADD FOREIGN KEY (`type_id`) REFERENCES `animal_types` (`id`);

ALTER TABLE `animal_colors` ADD FOREIGN KEY (`type_id`) REFERENCES `animal_types` (`id`);

ALTER TABLE `animal_genders` ADD FOREIGN KEY (`type_id`) REFERENCES `animal_types` (`id`);

ALTER TABLE `animal_breeds` ADD FOREIGN KEY (`type_id`) REFERENCES `animal_types` (`id`);
