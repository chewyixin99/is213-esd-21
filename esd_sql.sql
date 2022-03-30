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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `email`, `password`, `wallet_id`) VALUES
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
  `name` varchar(64) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `cuisine` varchar(64) NOT NULL,
  `course` varchar(64) NOT NULL,
  `vegetarian` BOOLEAN DEFAULT FALSE,
  
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`item_id`, `hawker_id`, `name`, `description`, `price`, `cuisine`, `course`, `vegetarian`) VALUES
('item_1', 'hawker_1', 'item_name_1', 'item_description_1', 1.0, 'chinese', 'main', TRUE), 
('item_2', 'hawker_2', 'item_name_2', 'item_description_2', 2.0, 'muslim', 'side', FALSE), 
('item_3', 'hawker_3', 'item_name_3', 'item_description_3', 3.0, 'indian', 'main', FALSE), 
('item_4', 'hawker_4', 'item_name_4', 'item_description_4', 4.0, 'korean', 'main', FALSE), 
('item_5', 'hawker_5', 'item_name_5', 'item_description_5', 5.0, 'any', 'drinks', TRUE);
COMMIT;

--
-- Table structure for table `wallet`
--
-- insert your code here 
--
-- Dumping data for table `wallet`
--


--
-- Table structure for table `order`
--
-- insert your code here 
--
-- Dumping data for table `order`
--


--
-- Table structure for table `escrow`
--
-- insert your code here 
--
-- Dumping data for table escrow`
--


--
-- Table structure for table `error`
--
-- insert your code here 
--
-- Dumping data for table `error`
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


