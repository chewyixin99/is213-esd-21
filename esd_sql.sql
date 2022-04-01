SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `ESD` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ESD`;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet_id` INT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE user AUTO_INCREMENT=1000;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `email`, `password`) VALUES
('customer_username_1', 'customer1@mail.com', 'customer_password_1'), 
('customer_username_2', 'customer2@mail.com', 'customer_password_2'),
('customer_username_3', 'customer3@mail.com', 'customer_password_3'),
('customer_username_4', 'customer4@mail.com', 'customer_password_4');
COMMIT;

DROP TABLE IF EXISTS `hawker`;
CREATE TABLE IF NOT EXISTS `hawker` (
  `hawker_id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet_id` INT DEFAULT NULL,
  `cuisine` varchar(64) NOT NULL,
  `halal` BOOLEAN DEFAULT FALSE,
  `has_vegetarian_option` BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE hawker AUTO_INCREMENT=2000;

--
-- Dumping data for table `user`
--

INSERT INTO `hawker` (`username`, `email`, `password`) VALUES
('hawker_username_1', 'hawker1@mail.com', 'hawker_password_1'), 
('hawker_username_2', 'hawker2@mail.com', 'hawker_password_2'),
('hawker_username_3', 'hawker3@mail.com', 'hawker_password_3'),
('hawker_username_4', 'hawker4@mail.com', 'hawker_password_4');
COMMIT;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `item_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `hawker_id` INT NOT NULL,
  `name` varchar(64) NOT NULL,
  `cuisine` varchar(64) NOT NULL,
  `description` varchar(255) NOT NULL,
  `course` varchar(64) NOT NULL,
  `price` float NOT NULL,
  `vegetarian` BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE item AUTO_INCREMENT=3000;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`hawker_id`, `name`, `description`, `price`, `cuisine`, `course`, `vegetarian`) VALUES
(2001, 'item_name_1', 'item_description_1', 1.0, 'chinese', 'main', TRUE), 
(2001, 'item_name_1', 'item_description_1_alt', 1.0, 'chinese', 'side', TRUE), 
(2002, 'item_name_2', 'item_description_2', 2.0, 'muslim', 'side', FALSE), 
(2003, 'item_name_3', 'item_description_3', 3.0, 'indian', 'main', FALSE), 
(2004, 'item_name_4', 'item_description_4', 4.0, 'korean', 'main', FALSE), 
(2005, 'item_name_5', 'item_description_5', 5.0, 'any', 'drinks', TRUE);
COMMIT;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `order_id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `hawker_id` INT NOT NULL,
  `status` varchar(16) NOT NULL,
  `total_price` float NOT NULL,
  `discount` float NOT NULL,
  `final_price` float NOT NULL,
  `items` varchar(255) NOT NULL,
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `order` AUTO_INCREMENT=4000;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`user_id`, `hawker_id`, `status`, `total_price`, `discount`, `final_price`, `items`) VALUES
(1000, 2001, "pending", 10, 5, 5, "[{'item_id': 3001, 'quantity': 1}, {'item_id': 3002, 'quantity': 1}]"),
(1000, 2000, "pending", 10, 0, 10, "[{'item_id': 3000, 'quantity': 2}, {'item_id': 3001, 'quantity': 1}, {'item_id': 3002, 'quantity': 1}, {'item_id': 3003, 'quantity': 1}, {'item_id': 3004, 'quantity': 1}]");
COMMIT;

--
-- Table structure for table `wallet`
--

DROP TABLE IF EXISTS `wallet`;
CREATE TABLE IF NOT EXISTS `wallet` (
  `wallet_id` INT PRIMARY KEY,
  `total_balance` float NOT NULL,
  `available_balance` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `wallet`
--

INSERT INTO `wallet` (`wallet_id`, `total_balance`, `available_balance`) VALUES
(1000, 0.0, 0.0),
(1001, 100.0, 95.0),
(2000, 36.9, 13.4),
(2001, 15.3, 12.4),
(1002, 1337.0, 42.0);
COMMIT;

--
-- Table structure for table `escrow`
--

DROP TABLE IF EXISTS `escrow`;
CREATE TABLE IF NOT EXISTS `escrow` (
  `order_id` INT PRIMARY KEY,
  `payer_id` INT NOT NULL,
  `receiving_id` INT NOT NULL,
  `amount` float NOT NULL,
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `escrow` <this shouldn't happen here, since escrow means got transactions.>
--

INSERT INTO `escrow` (`order_id`, `payer_id`, `receiving_id`, `amount`) VALUES
(4000, 1, 2, 1.0), -- check if can pay when person has no money
(4001, 2, 3, 1.0);
COMMIT;

--
-- Table structure for table `error`
--
-- insert table structure CODE here
--
-- Dumping data for table `error`
--
-- insert dumping data CODE here

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


