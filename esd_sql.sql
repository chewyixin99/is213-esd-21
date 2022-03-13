SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `ESD` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ESD`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `customer_id` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_id`, `username`, `email`, `password`, `wallet_id`) VALUES
('customer_1', 'customer_username_1', 'customer1@mail.com', 'customer_password_1', 'customer_wallet_1'), 
('customer_2', 'customer_username_2', 'customer2@mail.com', 'customer_password_2', 'customer_wallet_2'),
('customer_3', 'customer_username_3', 'customer3@mail.com', 'customer_password_3', 'customer_wallet_3'),
('customer_4', 'customer_username_4', 'customer4@mail.com', 'customer_password_4', 'customer_wallet_4');
COMMIT;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `item_id` varchar(64) NOT NULL,
  `hawker_id` varchar(64) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `cuisine_type` varchar(64) NOT NULL,
  `base` varchar(64) NOT NULL,
  `course_type` varchar(64) NOT NULL,
  
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`item_id`, `hawker_id`, `description`, `price`, `cuisine_type`, `base`, `course_type`) VALUES
('item_1', 'hawker_1', 'item_description_1', 1.0, 'chinese', 'rice', 'main'), 
('item_2', 'hawker_2', 'item_description_2', 2.0, 'muslim', 'rice', 'main'), 
('item_3', 'hawker_3', 'item_description_3', 3.0, 'indian', 'noodle', 'main'), 
('item_4', 'hawker_4', 'item_description_4', 4.0, 'korean', 'soup', 'main'), 
('item_5', 'hawker_5', 'item_description_5', 5.0, 'japanese', 'noodle', 'main');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
