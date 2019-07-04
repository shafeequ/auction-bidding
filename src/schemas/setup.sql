-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Jul 02, 2019 at 10:03 PM
-- Server version: 5.7.25
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `ki_connect`
--
CREATE DATABASE IF NOT EXISTS `ki_connect_2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ki_connect_2`;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(120) NOT NULL,
  `item_desc` varchar(250) NOT NULL,
  `item_base_price` decimal(10,4) NOT NULL,
  `item_bid_start_date` date NOT NULL,
  `item_bid_end_date` date NOT NULL,
  `item_created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `items`
--

INSERT INTO `items` ( `item_name`, `item_desc`, `item_base_price`, `item_bid_start_date`, `item_bid_end_date`, `item_created_date`) VALUES

('Book', 'Book desc ', '5', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('car', 'car desc ', '100', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('Bike', 'Bike desc ', '20', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('Fruit', 'Fruit desc ', '3', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('Smartphone', 'Smartphone desc ', '5', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('Beer', 'Beer desc ', '1', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('Perfume', 'Perfume desc ', '7', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57')
,('Raft', 'Raft desc ', '85', '2019-07-02', '2019-07-04', '2019-07-02 20:20:57');

-- --------------------------------------------------------

--
-- Table structure for table `items_sold`
--
-- this will have multiple rows for each bid 
CREATE TABLE `items_bidded` (
  `item_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `item_bidder_price` decimal(10,4) NOT NULL,
  `item_bid_date`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'user bid time '
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='which user brought which item on which date and for what val';

-- this will have  a single row user against item , helps in optimization and performance , we need not to refer that table for validation
CREATE TABLE `items_awarded` (
  `item_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `item_sold_price` decimal(10,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='this will have  a single row user against item , helps in optimization and performance , we need not to refer that table for validation';
-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'primary key',
  `user_name` varchar(250) NOT NULL COMMENT 'user name to display on the portal',
  `user_email` varchar(120) NOT NULL COMMENT 'user email id to be unique and can be used for logging purpose when used auth mechanism',
  `user_password` varchar(120) NOT NULL COMMENT 'password to use to login to the system later when auth is enabled',
  `user_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'user created date'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='holds the users in the auctioneer and bidding system';

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `user_name`, `user_email`, `user_password`, `user_created`) VALUES
(1, 'shafeeque', 'shafe786@gmail.com', '*5C62A0D136F04413028A98F50B274B06A26A8822', '2019-07-02 20:15:40'),
(2, 'bidder1', 'bidder1@gmail.com', '*372FE63E8B58B7479D9307C64A596954BCDA7DC0', '2019-07-02 20:15:40'),
(3, 'bidder2', 'bidder2@gmail.com', '*392BD20FE916EF5D54F44B8E6192474901AE2F9C', '2019-07-02 20:16:58'),
(4, 'bidder1', 'bidder3@gmail.com', '*A11ACF65EA2EAC2659FC34BAFA08CBD61CBD2587', '2019-07-02 20:16:58'),
(5, 'bidder4', 'bidder4@gmail.com', '*4D0ADA26EC946B143F071877F84D57538ECD2BA5', '2019-07-02 20:17:43'),
(6, 'bidder5', 'bidder5@gmail.com', '*E7048C8112BFC43599E8BC82502E1A2CAB4C7B50', '2019-07-02 20:17:43');

-- --------------------------------------------------------

--
-- Table structure for table `user_role`
--

CREATE TABLE `user_role` (
  `user_id` int(11) NOT NULL COMMENT 'user id',
  `user_role` tinyint(4) NOT NULL COMMENT 'user role 1=Auctioner 2=Bidder'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='table holds the user role types';

--
-- Dumping data for table `user_role`
--

INSERT INTO `user_role` (`user_id`, `user_role`) VALUES
(1, 1),
(2, 2),
(3, 2),
(4, 2),
(5, 2),
(6, 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_id`);

--
-- Indexes for table `items_sold` 
--
ALTER TABLE `items_bidded`
  ADD KEY `item_id` (`item_id`),
  ADD KEY `user_id` (`user_id`);


  ALTER TABLE `items_awarded`
  ADD KEY `item_id` (`item_id`),
  ADD KEY `user_id` (`item_sold_price`),
  ADD KEY `user_id` (`user_id`);

 CREATE UNIQUE INDEX idx_item_user ON items_awarded(item_id,user_id,item_sold_price); --
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- Indexes for table `user_role`
--
ALTER TABLE `user_role`
  ADD KEY `user_role` (`user_id`,`user_role`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'primary key', AUTO_INCREMENT=7;
COMMIT;
