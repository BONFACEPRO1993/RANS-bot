-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 04, 2018 at 05:17 PM
-- Server version: 5.7.17-log
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rans_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `captured_tweets1`
--

CREATE TABLE `captured_tweets1` (
  `id` int(11) NOT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `tweet` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `associated_url` varchar(200) NOT NULL,
  `created_time` datetime NOT NULL,
  `user_handle` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `user_name` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `captured_tweets1`
--


-- --------------------------------------------------------

--
-- Table structure for table `captured_tweets2`
--

CREATE TABLE `captured_tweets2` (
  `id` int(11) NOT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `tweet` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `associated_url` varchar(200) NOT NULL,
  `created_time` datetime NOT NULL,
  `user_handle` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `user_name` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `captured_tweets2`
--

I
-- --------------------------------------------------------

--
-- Table structure for table `rans_ersp_rec`
--

CREATE TABLE `rans_ersp_rec` (
  `message_id` bigint(30) NOT NULL,
  `message` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `ref_num` bigint(30) NOT NULL,
  `created_time` datetime NOT NULL,
  `source_handle` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `source_id` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rans_ersp_rec`
--


-- --------------------------------------------------------

--
-- Table structure for table `rans_ersp_send`
--

CREATE TABLE `rans_ersp_send` (
  `message_id` bigint(30) NOT NULL,
  `message` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `ref_num` bigint(30) NOT NULL,
  `created_time` datetime NOT NULL,
  `destination_handle` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `destination_id` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rans_ersp_send`
--


-- --------------------------------------------------------

--
-- Table structure for table `rans_informant_rec`
--

CREATE TABLE `rans_informant_rec` (
  `message_id` bigint(30) NOT NULL,
  `message` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `created_time` datetime NOT NULL,
  `source_handle` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `source_id` bigint(30) NOT NULL,
  `conf_status` int(11) NOT NULL DEFAULT '0',
  `valid_status` int(11) NOT NULL DEFAULT '0',
  `sent_status` int(11) NOT NULL DEFAULT '0',
  `replied_status` int(11) NOT NULL DEFAULT '0',
  `discard_status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rans_informant_rec`
--


-- --------------------------------------------------------

--
-- Table structure for table `rans_informant_send`
--

CREATE TABLE `rans_informant_send` (
  `message_id` bigint(30) NOT NULL,
  `message` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `ref_num` bigint(30) NOT NULL,
  `created_time` datetime NOT NULL,
  `destination_handle` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `destination_id` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rans_informant_send`
--


--
-- Indexes for dumped tables
--

--
-- Indexes for table `captured_tweets1`
--
ALTER TABLE `captured_tweets1`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tweet_id` (`tweet_id`);

--
-- Indexes for table `captured_tweets2`
--
ALTER TABLE `captured_tweets2`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tweet_id` (`tweet_id`);

--
-- Indexes for table `rans_ersp_rec`
--
ALTER TABLE `rans_ersp_rec`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `FK_MessageRefNum1` (`ref_num`);

--
-- Indexes for table `rans_ersp_send`
--
ALTER TABLE `rans_ersp_send`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `FK_MessageRefNum` (`ref_num`);

--
-- Indexes for table `rans_informant_rec`
--
ALTER TABLE `rans_informant_rec`
  ADD PRIMARY KEY (`message_id`);

--
-- Indexes for table `rans_informant_send`
--
ALTER TABLE `rans_informant_send`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `FK_MessageRefNum2` (`ref_num`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `captured_tweets1`
--
ALTER TABLE `captured_tweets1`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `captured_tweets2`
--
ALTER TABLE `captured_tweets2`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `rans_ersp_rec`
--
ALTER TABLE `rans_ersp_rec`
  ADD CONSTRAINT `FK_MessageRefNum1` FOREIGN KEY (`ref_num`) REFERENCES `rans_informant_rec` (`message_id`);

--
-- Constraints for table `rans_ersp_send`
--
ALTER TABLE `rans_ersp_send`
  ADD CONSTRAINT `FK_MessageRefNum` FOREIGN KEY (`ref_num`) REFERENCES `rans_informant_rec` (`message_id`);

--
-- Constraints for table `rans_informant_send`
--
ALTER TABLE `rans_informant_send`
  ADD CONSTRAINT `FK_MessageRefNum2` FOREIGN KEY (`ref_num`) REFERENCES `rans_informant_rec` (`message_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
