#!/usr/bin/env python

##################
# Python Imports #
##################


#################
# Local Imports #
#################

from ADPDException import ADPDException
from Logger import Logger

logger = Logger()


#############
# CONSTANTS #
#############


class DetectDP(object):
    """
    This class contains all the methods needed to analyze sub-patterns and extract design patterns from them
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def detect_singleton(self, sass_sub_pattern):
        """
        This method works on detecting singleton design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        singleton_dp = list()
        logger.info("Checking for Singleton Design Pattern")
        logger.info("Singleton can be founded by combination of SASS")
        for sass in sass_sub_pattern:
            dp = {"SASS": sass}
            logger.debug("Singleton DP in: %s" % str(dp))
            singleton_dp.append(dp)
        if len(singleton_dp):
            logger.info("Singleton design pattern has been detected: %s" % singleton_dp)
        else:
            logger.warning("Couldn't find any Singleton pattern in the code")
        return singleton_dp

    def detect_composite(self, sagg_sub_pattern, ci_sub_pattern, iiagg_sub_pattern, iagg_sub_pattern):
        """
        This method works on detecting composite design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        composite_dp = list()
        logger.info("Checking for Composite Design Pattern")
        logger.info("Composite can be founded by combination of SAGG, CI & IAGG, CI & IIAGG")
        logger.debug("Step1: checking for SAGG")
        if len(sagg_sub_pattern):
            for sagg in sagg_sub_pattern:
                dp = {"SAGG": sagg}
                logger.debug("Composite DP in: %s" % str(dp))
                composite_dp.append(dp)
        logger.debug("Step2: checking for CI & IAGG")
        if len(ci_sub_pattern) and len(iagg_sub_pattern):
            for ci in ci_sub_pattern:
                index = 0
                parent = ci[0]
                while index < len(iagg_sub_pattern):
                    comp = (iagg_sub_pattern[index][0], iagg_sub_pattern[index][1])[
                        parent == iagg_sub_pattern[index][0]]
                    if comp in ci:
                        dp = {"CI": ci, "IAGG": iagg_sub_pattern[index]}
                        logger.debug("Composite DP in: %s" % str(dp))
                        composite_dp.append(dp)
                    index = index + 1
        logger.debug("Step3: checking for CI & IIAGG")
        if len(ci_sub_pattern) and len(iiagg_sub_pattern):
            for ci in ci_sub_pattern:
                index = 0
                while index < len(iiagg_sub_pattern):
                    comp = iiagg_sub_pattern[index][2]
                    if comp in ci:
                        dp = {"CI": ci, "IIAGG": iagg_sub_pattern[index]}
                        logger.debug("Composite DP in: %s" % str(dp))
                        composite_dp.append(dp)
                    index = index + 1
        if len(composite_dp):
            logger.info("Composite design pattern has been detected: %s" % composite_dp)
        else:
            logger.warning("Couldn't find any composite pattern in the code")
        return composite_dp

    def detect_template(self, ci_sub_pattern):
        """
        This method works on detecting template design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        template_dp = list()
        logger.info("Checking for Template Design Pattern")
        logger.info("Template can be founded by combination of CI relation")
        for ci in ci_sub_pattern:
            dp = {"CI": ci}
            logger.debug("Template DP in: %s" % str(dp))
            template_dp.append(dp)
        if len(template_dp):
            logger.info("Template design pattern has been detected: %s" % template_dp)
        else:
            logger.warning("Couldn't find any Template pattern in the code")
        return template_dp

    def detect_adapter(self, ci_sub_pattern, ica_sub_pattern):
        """
        This method works on detecting adapter design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        adapter_dp = list()
        logger.info("Checking for Adapter Design Pattern")
        logger.info("Adapter can be founded by combination of ICA relation and a non-existance of CI relation")
        for dp in ica_sub_pattern:
            if dp not in ci_sub_pattern:
                logger.debug("Adapter DP in: %s" % str(dp))
                adapter = {"ICA": dp}
                adapter_dp.append(adapter)
        if len(adapter_dp):
            logger.info("Adapter design pattern has been detected: %s" % adapter_dp)
        else:
            logger.warning("Couldn't find any adapter pattern in the code")
        return adapter_dp

    def detect_bridge(self, ipag_sub_pattern, ci_sub_pattern):
        """
        This method works on detecting bridge design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        bridge_dp = list()
        logger.info("Checking for Bridge Design Pattern")
        logger.info("Bridge can be founded by combination of IPAG and CI")
        for ci in ci_sub_pattern:
            implementor = ci[0]
            ci1 = ci[1]
            ci2 = ci[2]
            for ipag in ipag_sub_pattern:
                if ci1 and ci2 not in ipag:
                    if implementor == ipag[2]:
                        dp = {"CI": ci, "IPAG": ipag}
                        logger.debug("Bridge DP in: %s" % str(dp))
                        bridge_dp.append(dp)
        if len(bridge_dp):
            logger.info("Bridge design pattern has been detected: %s" % bridge_dp)
        else:
            logger.warning("Couldn't find any bridge pattern in the code")
        return bridge_dp

    def detect_proxy(self, ci_sub_pattern, ica_sub_pattern, iass_sub_pattern):
        """
        This method works on detecting proxy design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        proxy_dp = list()
        logger.info("Checking for Proxy Design Pattern")
        logger.info("Proxy can be founded by combination of ICA & CI, CI & IASS")
        for ci in ci_sub_pattern:
            subject = ci[0]
            real_subject = ci[1]
            proxy = ci[2]
            for ica in ica_sub_pattern:
                if (subject == ica[0]) and (proxy and real_subject in (ica[1], ica[2])):
                    dp = {"ICA": ica, "CI": ci}
                    logger.debug("Proxy DP in: %s" % str(dp))
                    proxy_dp.append(dp)
            for iass in iass_sub_pattern:
                if (subject == iass[0]) and (proxy or real_subject in (iass[1])):
                    dp = {"IASS": iass, "CI": ci}
                    logger.debug("Proxy DP in: %s" % str(dp))
                    proxy_dp.append(dp)
        if len(proxy_dp):
            logger.info("Proxy design pattern has been detected: %s" % proxy_dp)
        else:
            logger.warning("Couldn't find any proxy pattern in the code")
        return proxy_dp

    def detect_decorator(self, ci_sub_pattern, iagg_sub_pattern, mli_sub_pattern):
        """
        This method works on detecting decorator design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        decorator_dp = list()
        logger.info("Checking for Decorator Design Pattern")
        logger.info("Decorator can be founded by combination of CI & IAGG & MLI")
        for mli in mli_sub_pattern:
            comp = mli[0]
            decorator = mli[1]
            for ci in ci_sub_pattern:
                if (comp == ci[0]) and (decorator in (ci[1], ci[2])):
                    for iagg in iagg_sub_pattern:
                        if comp == iagg[0] and decorator == iagg[1]:
                            dp = {"IAGG": iagg, "CI": ci, "MLI": mli}
                            logger.debug("Decorator DP in: %s" % str(dp))
                            decorator_dp.append(dp)
        if len(decorator_dp):
            logger.info("Decorator design pattern has been detected: %s" % decorator_dp)
        else:
            logger.warning("Couldn't find any decorator pattern in the code")
        return decorator_dp

    def detect_flyweight(self, ci_sub_pattern, agpi_sub_pattern):
        """
        This method works on detecting flyweight design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        flyweight_dp = list()
        logger.info("Checking for Flyweight Design Pattern")
        logger.info("Flyweight can be founded by combination of CI & AGPI")
        for ci in ci_sub_pattern:
            flyweight = ci[0]
            for agpi in agpi_sub_pattern:
                if flyweight == agpi[0] and agpi[1] in (ci[1], ci[2]) and agpi[2] not in (ci[1], ci[2]):
                    dp = {"AGPI": agpi, "CI": ci}
                    logger.debug("Flyweight DP in: %s" % str(dp))
                    flyweight_dp.append(dp)
        if len(flyweight_dp):
            logger.info("Flyweight design pattern has been detected: %s" % flyweight_dp)
        else:
            logger.warning("Couldn't find any flyweight pattern in the code")
        return flyweight_dp

    def detect_facad(self, icd_sub_pattern):
        """
        This method works on detecting facad design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        facad_dp = list()
        logger.info("Checking for Facad Design Pattern")
        logger.info("Facad can be founded by combination of triple ICD")
        for icd in icd_sub_pattern:
            parent = icd[0]
            child = icd[1]
            sub_system = icd[2]
            number_of_sub_system = 0
            icd_name = "ICD%s" % number_of_sub_system
            dp = {icd_name: icd}
            for inner_icd in icd_sub_pattern:
                if parent == inner_icd[0] and child == inner_icd[1] and sub_system != inner_icd[2]:
                    number_of_sub_system = number_of_sub_system + 1
                    icd_name = "ICD%s" % number_of_sub_system
                    dp[icd_name] = inner_icd
                if number_of_sub_system > 1:
                    if dp not in facad_dp:
                        facad_dp.append(dp)
                        logger.debug("Facad DP in: %s" % str(dp))
                    break
        if len(facad_dp):
            logger.info("Facad design pattern has been detected: %s" % facad_dp)
        else:
            logger.warning("Couldn't find any Facad pattern in the code")
        return facad_dp

    def detect_abstract_factory(self, dci_sub_pattern, icd_sub_pattern, ci_sub_pattern):
        """
        This method works on detecting abstract factory design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        abstract_factory_dp = list()
        logger.info("Checking for Abstract Factory Design Pattern")
        logger.info("Abstract Factory can be founded by combination of DCI & IDC & CI")
        for icd in icd_sub_pattern:
            concrete_factory = icd[1]
            product_a = icd[2]
            for dci in dci_sub_pattern:
                abstract_product = dci[0]
                product_b = dci[1]
                dci_concrete_factory = dci[2]
                if dci_concrete_factory == concrete_factory:
                    for ci in ci_sub_pattern:
                        if (ci[0] == abstract_product) and (product_a and product_b in (ci[1], ci[2])):
                            dp = {"ICD": icd, "DCI": dci, "CI": ci}
                            logger.debug("Abstract Factory DP in: %s" % str(dp))
                            abstract_factory_dp.append(dp)
        if len(abstract_factory_dp):
            logger.info("Abstract Factory design pattern has been detected: %s" % abstract_factory_dp)
        else:
            logger.warning("Couldn't find any Abstract Factory pattern in the code")
        return abstract_factory_dp

    def detect_builder(self, ica_sub_pattern, agpi_sub_pattern):
        """
        This method works on detecting builder design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        builder_dp = list()
        logger.info("Checking for Builder Design Pattern")
        logger.info("Builder can be founded by combination of IDA & AGPI")
        for ica in ica_sub_pattern:
            builder = ica[0]
            concrete_builder = ica[1]
            product = ica[2]
            for agpi in agpi_sub_pattern:
                if agpi[0] == builder and agpi[1] == concrete_builder and agpi[2] != product:
                    dp = {"ICA": ica, "AGPI": agpi}
                    logger.debug("Builder DP in: %s" % str(dp))
                    builder_dp.append(dp)
        if len(builder_dp):
            logger.info("Builder design pattern has been detected: %s" % builder_dp)
        else:
            logger.warning("Couldn't find any Builder pattern in the code")
        return builder_dp

    def detect_factory(self, icd_sub_pattern, dci_sub_pattern):
        """
        This method works on detecting factory design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        factory_dp = list()
        logger.info("Checking for Factory Design Pattern")
        logger.info("Factory can be founded by combination of ICD & DCI")
        for dci in dci_sub_pattern:
            concrete_product = dci[1]
            concrete_creator = dci[2]
            for icd in icd_sub_pattern:
                if icd[1] == concrete_creator and icd[2] == concrete_product and icd[0] not in dci:
                    dp = {"ICD": icd, "DCI": dci}
                    logger.debug("Factory DP in: %s" % str(dp))
                    factory_dp.append(dp)
        if len(factory_dp):
            logger.info("Factory design pattern has been detected: %s" % factory_dp)
        else:
            logger.warning("Couldn't find any Factory pattern in the code")
        return factory_dp

    def detect_prototype(self, ci_sub_pattern, agpi_sub_pattern):
        """
        This method works on detecting prototype design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        prototype_dp = list()
        logger.info("Checking for Prototype Design Pattern")
        logger.info("Prototype can be founded by combination of CI & AGPI")
        for agpi in agpi_sub_pattern:
            prototype = agpi[0]
            con_proto_a = agpi[1]
            for ci in ci_sub_pattern:
                if prototype == ci[0] and con_proto_a in ci and agpi[2] not in ci:
                    dp = {"CI": ci, "AGPI": agpi}
                    logger.debug("Prototype DP in: %s" % str(dp))
                    prototype_dp.append(dp)
        if len(prototype_dp):
            logger.info("Prototype design pattern has been detected: %s" % prototype_dp)
        else:
            logger.warning("Couldn't find any Prototype pattern in the code")
        return prototype_dp

    def detect_chain_of_responsibility(self, sass_sub_pattern, ci_sub_pattern):
        """
        This method works on detecting prototype design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        chain_of_responsibility_dp = list()
        logger.info("Checking for Chain of Responsibility Design Pattern")
        logger.info("Chain of Responsibility can be founded by combination of SASS & CI")
        for sass in sass_sub_pattern:
            for ci in ci_sub_pattern:
                if sass[0] == ci[0]:
                    dp = {"SASS": sass, "CI": ci}
                    logger.debug("Chain of Responsibility DP in: %s" % str(dp))
                    chain_of_responsibility_dp.append(dp)
        if len(chain_of_responsibility_dp):
            logger.info("Chain of Responsibility design pattern has been detected: %s" % chain_of_responsibility_dp)
        else:
            logger.warning("Couldn't find any Chain of Responsibility pattern in the code")
        return chain_of_responsibility_dp

    def detect_command(self, agpi_sub_pattern, ica_sub_pattern):
        """
        This method works on detecting command design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        command_dp = list()
        logger.info("Checking for Command Design Pattern")
        logger.info("Command can be founded by combination of ICA & AGPI")
        for agpi in agpi_sub_pattern:
            command = agpi[0]
            conc_command = agpi[1]
            for ica in ica_sub_pattern:
                if command == ica[0] and conc_command == ica[1] and agpi[2] != ica[2]:
                    dp = {"ICA": ica, "AGPI": agpi}
                    logger.debug("Command DP in: %s" % str(dp))
                    command_dp.append(dp)
        if len(command_dp):
            logger.info("Command design pattern has been detected: %s" % command_dp)
        else:
            logger.warning("Couldn't find any Command pattern in the code")
        return command_dp

    def detect_interpreter(self, iagg_sub_pattern, ipd_sub_pattern, ci_sub_pattern):
        """
        This method works on detecting interpreter design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        interpreter_dp = list()
        logger.info("Checking for Interpreter Design Pattern")
        logger.info("Interpreter can be founded by combination of IAGG & CI & IPD")
        for iagg in iagg_sub_pattern:
            abstract_expression = iagg[0]
            nonterminatl_expression = iagg[1]
            for ipd in ipd_sub_pattern:
                content = ipd[2]
                if abstract_expression == ipd[0]:
                    for ci in ci_sub_pattern:
                        if abstract_expression == ci[0] and nonterminatl_expression in ci and content not in ci:
                            dp = {"IAGG": iagg, "IPD": ipd, "CI": ci}
                            logger.debug("Interpreter DP in: %s" % str(dp))
                            interpreter_dp.append(dp)
        if len(interpreter_dp):
            logger.info("Interpreter design pattern has been detected: %s" % interpreter_dp)
        else:
            logger.warning("Couldn't find any Interpreter pattern in the code")
        return interpreter_dp

    def detect_iterator(self, dci_sub_pattern, ica_sub_pattern, icd_sub_pattern):
        """
        This method works on detecting iterator design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        iterator_dp = list()
        logger.info("Checking for Iterator Design Pattern")
        logger.info("Iterator can be founded by combination of ICD & DCI & ICA")
        for ica in ica_sub_pattern:
            iterator = ica[0]
            conc_iterator = ica[1]
            conc_agg = ica[2]
            for dci in dci_sub_pattern:
                if iterator == dci[0] and conc_iterator == dci[1] and conc_agg == dci[2]:
                    for icd in icd_sub_pattern:
                        if conc_agg == icd[1] and conc_iterator == icd[2] and icd[0] not in ica:
                            dp = {"DCI": dci, "ICA": ica, "ICD": icd}
                            logger.debug("Iterator DP in: %s" % str(dp))
                            iterator_dp.append(dp)
        if len(iterator_dp):
            logger.info("Iterator design pattern has been detected: %s" % iterator_dp)
        else:
            logger.warning("Couldn't find any Iterator pattern in the code")
        return iterator_dp

    def detect_mediator(self, ica_sub_pattern, ci_sub_pattern, ipas_sub_pattern):
        """
        This method works on detecting mediator design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        mediator_dp = list()
        logger.info("Checking for Mediator Design Pattern")
        logger.info("Mediator can be founded by combination of CI & IPAS & ICA")
        for ica in ica_sub_pattern:
            mediator = ica[0]
            conc_colleague_a = ica[2]
            for ipas in ipas_sub_pattern:
                if mediator == ipas[2]:
                    colleague = ipas[0]
                    conc_colleague_b = ipas[1]
                    for ci in ci_sub_pattern:
                        if colleague == ci[0] and (conc_colleague_a and conc_colleague_b in ci):
                            dp = {"CI": ci, "ICA": ica, "IPAS": ipas}
                            logger.debug("Mediator DP in: %s" % str(dp))
                            mediator_dp.append(dp)
        if len(mediator_dp):
            logger.info("Mediator design pattern has been detected: %s" % mediator_dp)
        else:
            logger.warning("Couldn't find any Mediator pattern in the code")
        return mediator_dp

    def detect_memento(self, agpi_sub_pattern, dpi_sub_pattern):
        """
        This method works on detecting memento design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        memento_dp = list()
        logger.info("Checking for Memento Design Pattern")
        logger.info("Memento can be founded by combination of AGPI & DPI")
        for agpi in agpi_sub_pattern:
            memento = agpi[0]
            memento_imp = agpi[1]
            for dpi in dpi_sub_pattern:
                if memento == dpi[0] and memento_imp == dpi[1] and agpi[2] != dpi[2]:
                    dp = {"AGPI": agpi, "DPI": dpi}
                    logger.debug("Memento DP in: %s" % str(dp))
                    memento_dp.append(dp)
        if len(memento_dp):
            logger.info("Memento design pattern has been detected: %s" % memento_dp)
        else:
            logger.warning("Couldn't find any Memento pattern in the code")
        return memento_dp

    def detect_observer(self, agpi_sub_pattern, icd_sub_pattern):
        """
        This method works on detecting observer design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        observer_dp = list()
        logger.info("Checking for Observer Design Pattern")
        logger.info("Observer can be founded by combination of AGPI & ICD")
        for icd in icd_sub_pattern:
            observer = icd[0]
            conc_observer = icd[1]
            conc_subject = icd[2]
            for agpi in agpi_sub_pattern:
                if observer == agpi[0] and conc_observer == agpi[1] and conc_subject != agpi[2]:
                    dp = {"AGPI": agpi, "ICD": icd}
                    logger.debug("Observer DP in: %s" % str(dp))
                    observer_dp.append(dp)
        if len(observer_dp):
            logger.info("Observer design pattern has been detected: %s" % observer_dp)
        else:
            logger.warning("Couldn't find any Observer pattern in the code")
        return observer_dp

    def detect_state(self, agpi_sub_pattern, ci_sub_pattern):
        """
        This method works on detecting state design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        state_dp = list()
        logger.info("Checking for State Design Pattern")
        logger.info("State can be founded by combination of AGPI & CI")
        for agpi in agpi_sub_pattern:
            state = agpi[0]
            conc_state_a = agpi[1]
            for ci in ci_sub_pattern:
                if state == ci[0] and conc_state_a in ci:
                    dp = {"AGPI": agpi, "CI": ci}
                    logger.debug("State DP in: %s" % str(dp))
                    state_dp.append(dp)
        if len(state_dp):
            logger.info("State design pattern has been detected: %s" % state_dp)
        else:
            logger.warning("Couldn't find any State pattern in the code")
        return state_dp

    def detect_strategy(self,agpi_sub_pattern, ci_sub_pattern):
        """
        This method works on detecting strategy design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        strategy_dp = list()
        logger.info("Checking for Strategy Design Pattern")
        logger.info("Strategy can be founded by combination of AGPI & CI")
        for agpi in agpi_sub_pattern:
            strategy = agpi[0]
            conc_strategy_a = agpi[1]
            for ci in ci_sub_pattern:
                if strategy == ci[0] and conc_strategy_a in ci:
                    dp = {"AGPI": agpi, "CI": ci}
                    logger.debug("Strategy DP in: %s" % str(dp))
                    strategy_dp.append(dp)
        if len(strategy_dp):
            logger.info("Strategy design pattern has been detected: %s" % strategy_dp)
        else:
            logger.warning("Couldn't find any Strategy pattern in the code")
        return strategy_dp

    def detect_visitor(self, agpi_sub_pattern, icd_sub_pattern, dpi_sub_pattern):
        """
        This method works on detecting visitor design pattern and return if this patterns
        exists or not
        :return: DP location
        """
        visitor_dp = list()
        logger.info("Checking for Visitor Design Pattern")
        logger.info("Visitor can be founded by combination of AGPI & ICD & DPI")
        for icd in icd_sub_pattern:
            visitor = icd[0]
            conc_visitor = icd[1]
            conc_element = icd [2]
            for dpi in dpi_sub_pattern:
                if visitor == dpi[0] and conc_visitor == dpi[1]:
                    for agpi in agpi_sub_pattern:
                        if conc_element == agpi[1] and dpi[2] == agpi[0]:
                            dp = {"AGPI": agpi, "DPI": dpi, "ICD": icd}
                            logger.debug("Visitor DP in: %s" % str(dp))
                            visitor_dp.append(dp)
        if len(visitor_dp):
            logger.info("Visitor design pattern has been detected: %s" % visitor_dp)
        else:
            logger.warning("Couldn't find any Visitor pattern in the code")
        return visitor_dp

